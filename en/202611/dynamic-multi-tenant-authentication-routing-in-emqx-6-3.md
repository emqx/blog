## Introduction

A multi-tenant MQTT platform often needs to authenticate devices against separate identity services while sharing a common broker infrastructure. Maintaining separate authentication configurations for each tenant or adding an intermediary to route requests can increase operational complexity.

[EMQX Enterprise 6.3](https://www.emqx.com/en/blog/emqx-6-3-0-release-notes) supports client attributes in the hostnames of HTTP authentication and authorization URLs. This allows a shared configuration to route requests to tenant-specific backends based on connection attributes, while request headers supply the corresponding service credentials.

In this article, we'll configure dynamic HTTP routing for two tenants, cover both authentication and authorization, and test tenant isolation with a runnable example.

## Route Each Tenant to Its Own Service



A fixed HTTP endpoint needs a routing layer if checks must reach different tenant services. EMQX can now render the destination hostname directly from connection attributes:

```
https://${client_attrs.tenant}.auth.example.com/authn
```

For an illustrative platform with two tenants, `north` and `south`, the mapping looks like this:

| MQTT username    | Tenant attribute | Authentication endpoint                  |
| :--------------- | :--------------- | :--------------------------------------- |
| `north/device17` | `north`          | `<https://north.auth.example.com/authn`> |
| `south/device42` | `south`          | `<https://south.auth.example.com/authn`> |

The broker extracts the tenant prefix before authentication, then uses it to build the HTTP request. Each service checks the device against its own records. This removes the need for an intermediary whose only job is forwarding authentication requests to the right tenant.

The tenant prefix selects the destination. The service must still validate the device's credentials and membership in that tenant; putting `north` in a username does not grant access to North's devices or topics.

## Configure the Endpoint and Its Service Credential



There are two credentials in this exchange. The MQTT device supplies its own login credential. EMQX supplies a separate API key identifying the broker to the tenant's HTTP service. The device does not need that API key.

For this example, supply the tenant API keys through the EMQX process environment before starting the node:

```
export EMQXVAR_north_auth_token='<north-service-api-key>'
export EMQXVAR_south_auth_token='<south-service-api-key>'
```

In a container deployment, inject these values through the deployment's secret mechanism. The names above are examples; use actual service credentials in the environment.

Add the following configuration to `base.hocon`. It extracts the tenant and looks up its service key, then uses both in an HTTP authenticator. It assumes an existing MQTT listener and two HTTPS authentication services. Replace the example domains and mount the CA bundle that validates their certificates at the configured path.

```
mqtt.client_attrs_init = [
  {
    expression = "nth(1, tokens(username, '/'))"
    set_as_attr = tenant
  },
  {
    expression = "getenv(concat([nth(1, tokens(username, '/')), '_auth_token']))"
    set_as_attr = auth_token
  }
]

authentication = [
  {
    mechanism = password_based
    backend = http
    method = post
    url = "https://${client_attrs.tenant}.auth.example.com/authn"
    hostname_resolution = dynamic
    allowed_hosts = [
      "north.auth.example.com",
      "south.auth.example.com"
    ]
    headers {
      "Content-Type" = "application/json"
      "X-API-Key" = "${client_attrs.auth_token}"
    }
    body {
      username = "${username}"
      password = "${password}"
      clientid = "${clientid}"
    }
    ssl {
      enable = true
      verify = verify_peer
      cacertfile = "/opt/emqx/etc/certs/auth-ca.pem"
    }
  }
]
```

The `getenv()` function adds the `EMQXVAR_` prefix. For `north/device17`, the expression reads `EMQXVAR_north_auth_token`. Both initializer expressions derive the tenant from the username because one initializer cannot use an attribute produced by another.

`hostname_resolution = dynamic` enables the templated host. The `allowed_hosts` list restricts which destinations the template may produce. EMQX applies TLS verification to the rendered hostname. A hostname outside the list receives no request.

### Follow an Authentication Request



For an uncached authentication check from `north/device17`, EMQX sends a POST request to `<https://north.auth.example.com/authn`.> Its JSON body contains the device's username, password and client ID. The `X-API-Key` header contains North's broker-to-service credential.

North's service validates the API key and the device login. To accept the connection, it returns HTTP `200` with `content-type: application/json` and:

```json
{
  "result": "allow",
  "is_superuser": false
}
```

For an invalid login, it returns `{"result":"deny"}`. Keeping `is_superuser` false ensures the client remains subject to MQTT authorization checks.

For EMQX 6.3.0 and 6.3.1, send the response header name `content-type` in lowercase. The dynamic HTTP response parser in these versions expects that spelling; the runnable example below includes this compatibility detail.

### Operate the Credential Lookup



Environment-based lookup fits credentials managed through the deployment process. `getenv()` caches values once read, so changing a service key in this example requires updating the node's environment and restarting it. Updating a container's secret definition alone does not refresh a running node's cached value.

The example stores the key in a client attribute. That attribute can appear in administrative diagnostics and debug logs, so restrict access to those surfaces and avoid logging the value. Treat this as a deployment-managed credential lookup, with an explicit rotation procedure.

## Route Publish and Subscribe Checks Too



The same hostname and header templates work for HTTP authorization. After a device connects, its tenant service can decide whether an operation on a particular topic is permitted.

Using the attributes initialized above, configure the HTTP authorization source as follows:

```
authorization {
  no_match = deny
  sources = [
    {
      type = http
      method = post
      url = "https://${client_attrs.tenant}.auth.example.com/authz"
      hostname_resolution = dynamic
      allowed_hosts = [
        "north.auth.example.com",
        "south.auth.example.com"
      ]
      headers {
        "Content-Type" = "application/json"
        "X-API-Key" = "${client_attrs.auth_token}"
      }
      body {
        username = "${username}"
        clientid = "${clientid}"
        action = "${action}"
        topic = "${topic}"
      }
      ssl {
        enable = true
        verify = verify_peer
        cacertfile = "/opt/emqx/etc/certs/auth-ca.pem"
      }
    }
  ]
}
```

When a publish check for `north/device17` reaches this source, the request goes to North's `/authz` endpoint with the action `publish` and the requested topic. The service evaluates that operation against the device's permissions and returns HTTP `200` with a JSON `result` of `allow` or `deny`.

`no_match = deny` rejects operations that no source allows. For an explicit policy rejection, return `deny`; `ignore` lets evaluation continue. Authorization caching still governs when a backend check is needed, so account for it when choosing how quickly permission changes must take effect.

Here, `tenant` is a routing attribute. The platform's topic permissions and any configured EMQX namespaces still determine message isolation. The authentication and authorization definitions remain shared broker configuration; tenant-specific identity and permission decisions live in the selected services.

## Try the Runnable Example



The [two-tenant example](https://github.com/emqx/emqx-usage-example/tree/main/dynamic-tenant-auth) includes EMQX 6.3.1, separate North and South HTTPS services, generated test certificates, and automated MQTT 5 tests. From the example directory, run:

```
docker compose up -d --build --wait emqx
docker compose run --rm --no-deps tests
```

The tests check successful connections and message delivery within each tenant, rejected cross-tenant operations, invalid credentials, and blocked destinations. They also verify that a rejected service key or an HTTP 503 response denies access for the affected tenant while the other continues working.

Use `docker compose logs north-auth south-auth` to follow the routing decisions. The service logs show the destination, action, and result without printing device passwords or API keys. Run `docker compose down -v` to remove the example and its generated certificates.

## Onboard the Next Tenant



For a third tenant such as `east`, provision its auth service and certificate, add `east.auth.example.com` to both allow lists, and supply its service API key to the broker deployment. The URL and header templates stay the same.

You can apply the updated configuration and environment through a rolling restart. For onboarding without a restart, update the allow lists at runtime. The new tenant's key must also be present in every running node's environment before its first `getenv()` lookup. If the key was not supplied at startup, set it on each node:

```
emqx eval 'os:putenv("EMQXVAR_east_auth_token", "<east-service-api-key>").'
```

Run this on every node before accepting connections for `east`: an earlier lookup can already have cached an empty value. The command affects only the addressed node and does not persist across restarts, so also save the key in the deployment's secret configuration. Literal keys in `emqx eval` expressions can be recorded in shell history and, when enabled, EMQX audit logs.

After either path, verify both accepted and rejected connections and topic operations.

## Simplify Multi-Tenant MQTT Authentication with EMQX 6.3



EMQX Enterprise 6.3 allows a shared HTTP authentication and authorization configuration to route requests to tenant-specific backends using client attributes. This enables multi-tenant MQTT platforms to reuse existing identity and permission services without maintaining a duplicate device credential database or building a separate authentication router.

For production deployments, combine dynamic routing with explicit hostname allowlists, verified TLS connections, secure service-credential management, and tenant-specific authorization policies.

For further details, see the official documentation:

- [HTTP Authentication: Configure Dynamic Hostname Resolution](https://docs.emqx.com/en/emqx/latest/guides/access-control/authn/http.html#configure-dynamic-hostname-resolution)
- [HTTP Authorization: Configure Dynamic Hostname Resolution](https://docs.emqx.com/en/emqx/latest/guides/access-control/authz/http.html#configure-dynamic-hostname-resolution)

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
