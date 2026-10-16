>**At a glance**
>
>- [EMQX 6.3](https://www.emqx.com/en/blog/emqx-6-3-0-release-notes) introduces **security profiles**. One setting switches a node between two sets of security defaults: `legacy` and `hardened`.
>- The **hardened** profile gives you secure-by-default behavior across the whole broker. We recommend it for every new deployment.
>- The **legacy** profile keeps the behavior you know. It stays the default in EMQX 6.x, so upgrades and existing integrations keep working.
>- **EMQX 7.0 will use the hardened profile by default.** Existing deployments can keep the legacy profile with one line of configuration.

## Security Should Not Depend on a Checklist

EMQX gives operators multiple ways to secure a deployment, including authentication, authorization, TLS, and more. But effective security depends on getting many settings right, and every deployment starts with its defaults. Defaults designed for a quick start are convenient on day one, but production environments need defaults that prioritize safety.

Until now, securing a deployment meant finding and adjusting these settings one bye one yourself. **EMQX 6.3 changes that with a simpler approach**: one setting enables secure defaults across the entire node, giving every new deployment a stronger security baseline from the start.

## Two Profiles, One Choice



| Profile      | What it does                                                 | When to use it                                               |
| :----------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Hardened** | Applies strict, secure-by-default behavior across the broker. | New deployments, and existing deployments once they have been reviewed. |
| **Legacy**   | Keeps the default behavior of earlier EMQX versions.         | Upgrades from earlier versions, and integrations that depend on the earlier behavior. |

A profile only changes *defaults*. You can still configure each behavior on its own. For example, a hardened node can still allow anonymous clients on one listener when you choose to allow them. The difference is that you make that choice on purpose.

## What the Hardened Profile Brings



The hardened profile follows one principle: **nothing is open unless you open it**. In practice, this means:

- **No shared default secrets.** A node does not start with well-known sample credentials, and Dashboard accounts cannot keep the factory default password. Every deployment uses secrets of its own.
- **No accidental exposure.** MQTT listeners and the Dashboard accept only local connections until you decide which network interfaces they should serve.
- **Authentication is explicit.** Clients must authenticate unless you have explicitly allowed anonymous access.
- **Access is denied when in doubt.** When an authentication or authorization service is unavailable or returns an unexpected answer, EMQX denies the request instead of letting it through.
- **Deny-by-default authorization.** Clients can publish and subscribe only where your rules allow them.
- **Trusted connections and packages.** EMQX verifies the servers it contacts for authentication keys, and installs a plugin only when the package matches the one an administrator approved.
- **Consistent checks everywhere.** Access rules also apply to messages scheduled for later delivery and to subscriptions that EMQX creates on behalf of clients.

Each item is a small change. Together, they mean that a new deployment starts in a safe state, and that every opening is a decision you made.

## Legacy Mode: Upgrade Without Surprises



We know that many EMQX deployments are part of larger systems. Devices, backend services, scripts, and monitoring tools may rely on how EMQX behaves today. A change of defaults should never break them without warning.

That’s why EMQX 6.x keeps the **legacy profile as the default**. When you upgrade to EMQX 6.3, your existing deployment continues to behave as before: no configuration changes are required. 

Keep the legacy profile when:

- You run a rolling upgrade from a version earlier than 6.3, so that all nodes behave the same during the upgrade;
- Your devices or integrations depend on the earlier behavior, and you have not reviewed them yet;
- You need time to plan the move to the hardened profile.

The legacy profile is a fully supported choice, not a workaround.

## Easy to Adopt



Selecting a profile takes one setting. Add the following line to the EMQX environment file, or pass it as an environment variable to a container, and restart the node:

```
EMQX_SECURITY_PROFILE=hardened
```

To keep the earlier behavior, use `legacy` instead. Use the same profile on every node in a cluster. The EMQX Dashboard shows the active profile of each node, so you can confirm at a glance that the whole cluster is consistent.

To move an existing deployment to the hardened profile:

1. Complete any rolling upgrade to EMQX 6.3 with the legacy profile.
2. Review the list of hardened behaviors in the documentation and decide which ones need an explicit setting in your deployment.
3. Replace any default secrets and passwords.
4. Confirm which network interfaces your listeners and Dashboard should serve.
5. Switch to the hardened profile and restart the nodes one at a time.

The [Security Profiles documentation](https://docs.emqx.com/en/emqx/latest/guides/access-control/security-profile.html) describes every behavior change and the setting that controls it.

## What’s Next: Hardened by default in EMQX 7.0



EMQX 6.3 gives you a transition period to adopt the hardened profile on your own schedule. Starting with **EMQX 7.0, the hardened profile will be the default**. New installations of EMQX 7.0 will be secure by default from the first start.

If you want to keep the current behavior when you move to EMQX 7.0, set the profile to legacy before you upgrade. This takes one line of configuration, and your deployment continues to work as it does today.

We recommend using the time before EMQX 7.0 to try the hardened profile. Start with a test or staging environment, review what changes for your devices and integrations, and move to production when you are ready.

## Conclusion



Security profiles make a secure EMQX deployment the easy path. The hardened profile gives you safe defaults with one setting. The legacy profile keeps your upgrades and integrations working while you prepare. With EMQX 7.0, secure-by-default becomes the standard for every new installation.

Try the hardened profile in EMQX 6.3 today. If you have questions about moving your deployment, [contact our team](https://www.emqx.com/en/contact).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
