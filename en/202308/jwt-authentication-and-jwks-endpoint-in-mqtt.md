Authentication is an important means to ensure the security of [MQTT services](https://www.emqx.com/en/cloud). [EMQX](https://www.emqx.com/en/products/emqx) provides various authentication methods, such as Password-Based Authentication, Token-Based Authentication, and Enhanced Authentication for users to choose. 

This article will introduce the basic principles of Token-Based Authentication based on JWT (JSON Web Token, an open standard that defines how to pass JSON objects between web applications), and how to build your own JWKS Endpoint.

## What is Token-Based Authentication?

When we use Password-Based Authentication in EMQX, the client will be authenticated by EMQX. Token-Based Authentication allows us to hand over the identity verification work to an independent authentication server without exposing the username and password to EMQX, and we don't need to re-authenticate before the token granted by the authentication server expires.

Its complete process can be summarized as the following four steps:

1. The [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) first initiates an authentication request to the authentication server with user credentials such as username and password.
2. The authentication server verifies the user credentials held by the client, issues a **token,** and returns it to the client after passing the verification.
3. The client uses the **token** granted by the authentication server to initiate a connection request to the [MQTT server](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).
4. The MQTT server will check the **token** held by the client to confirm whether the authentication server signs it and whether the content has been tampered with. After the check is passed, the client will be allowed to connect.

![Token-Based Authentication](https://assets.emqx.com/images/24afb3bb3d6a8936f14c86da166b797d.png)

## Token-Based Authentication Based on JWT

Therefore, the key point of Token-Based Authentication is that the MQTT server must be able to confirm that the token held by the client is issued by the authentication server and not forged by a third party. And it must also be able to verify that the content of token hasn't been tampered with.

A common method is to use JWT as the token. We can let the authentication server apply a signature to the content of JWT so that we can check the integrity and source of JWT. Common ways to generate signatures include Message Authentication Code (MAC) and Digital Signature, but we generally recommend using the latter for security reasons.

### Message Authentication Code (MAC)

The principle of Message Authentication Code is to use a secret key to calculate the MAC value for the given input. With the same key, different inputs will produce different MAC values. And with the same input, different keys will also result in different MAC values.

So we can let the authentication server and the MQTT server share a key. The authentication server uses this key to calculate the MAC for the JWT content, then appends it to the content. After receiving the JWT, the MQTT server also uses its key to calculate the content's MAC value, then compares it with the MAC value in the JWT. If the two are consistent, the messages have not been tampered with, and the issuer holds the correct key.

![Message Authentication Code (MAC)](https://assets.emqx.com/images/21d1ccd02f20235c20a1db19ae703b31.png)

HMAC(Hash-Baed Message Authentication Code) is a common method of using a one-way hash function to construct the message authentication code. According to the different SHA functions, it is divided into HS256, HS384, and so on.

But the disadvantage of Message Authentication Code is also obvious. We have to share the key with all JWT verifiers, which increases the risk of key leakage. And once the verifier holds the key, it also can issue JWT. So we can only know that the issuer possesses the correct key, but we can't guarantee that it must be the authentication server.

### Digital Signature

Given the issues present in Message Authentication Code, we usually recommend using Digital Signatures instead. The authentication server uses a private key to generate a signature, and the MQTT server uses a public key to verify the signature. We can share the public key with anyone, but they will only have the ability to verify signatures, not the ability to generate signatures.

So as long as the private key held by the authentication server is not leaked, we can assume that the JWT with a valid signature must be issued by the authentication server. Common Digital Signature algorithms include RSA, ECDSA, etc.

## Generate a Signature for JWT

The signature will be included directly in the JWT to facilitate peer verification. JWT is separated by `.` into three parts, which are Header, Payload and Signature. The object we signed is the Header and Payload part.

To allow JWT to be better transmitted in the network, these three parts will eventually be encoded by Base64Url. So usually the JWT we see is like this:

```
base64UrlEncode(Header) + "." + base64UrlEncode(Payload) + "." + base64UrlEncode(Signature)
```

### Header

The Header is a JSON object, which usually consists of two parts: the type of token and the signature algorithm used, such as HS256, RS256, etc.

```
{
  "typ": "JWT",
  "alg": "HS256"
}
```

A complete list of JWT signature algorithms can be found in [RFC7518](https://www.rfc-editor.org/rfc/rfc7518).

### Payload

The Payload following the Header is also a JSON object used to carry the various claims we need to pass. We can use JWT predefined claims, which generally have a definite purpose and data type. For example, the "iat” claim is used to record the issuance time of the current token, and the "exp” claim is used to indicate the expiration time of the current token. We can also use custom claims using arbitrary names and data types.

The following example includes a predefined claim and a custom claim:

```
{
  "name": "John Doe",
  "iat": 1516239022
}
```

### Signature

Now, we need to generate a signature to the previous Header and Payload to prevent data tampering.

Taking HS256 as an example, the way to generate a signature is as follows:

```
HMACSHA256(base64UrlEncode(Header) + "." + base64UrlEncode(Payload), Secret)
```

We can use the [JWT.IO](https://jwt.io/)  tool to generate a JWT for the above. When we use the HS256 algorithm and specify the key as `emqx`, we will get the following JWT:

![JWT](https://assets.emqx.com/images/2a78c5e108660261a6ce153ae6749a44.png)

Then we can use the following Python code to calculate the signature for the same Header and Payload and compare it with the signature given by [JWT.IO](https://jwt.io/):

```
import base64
import hmac
from hashlib import sha256

# Replace it with your secret
secret = "emqx".encode('utf-8')
# Replace it with the header given by jwt.io
base64_header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
# Replace it with the payload given by jwt.io
base64_payload = "eyJuYW1lIjoiSm9obiBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9"
# Replace it with the signature given by jwt.io
base64_signature = "4AE9JkW8rrIDI5WC5gyo3wZU5vG34as566LtNfBFoVo"

msg = (base64_header + "." + base64_payload).encode('utf-8')
signature = str(base64.urlsafe_b64encode(hmac.new(secret, msg, sha256).digest()), 'utf-8')
# Remove the padding and compare
if signature.replace('=', '') == base64_signature:
  print("Matched")
else:
  print("UnMatched")
```

Now we know what JWT is and how to generate a signature for a JWT. Please note that the signature does not encrypt the content of the JWT, which is why we do not recommend carrying sensitive data in the JWT. In addition, to prevent JWT leakage, we strongly advise encrypting the client's connections to both the authentication server and the MQTT server using TLS.

## What is JWKS Endpoint?

No matter which signature algorithm we use, there is a risk of key leakage. So it is better to rotate or update the key regularly. But manually configuring new keys into the server is not a good choice, especially when multiple servers use the same set of keys. In a multi-tenant scenario, we may also need to provide different keys for different tenants.

We need a more efficient mechanism for managing and distributing keys, and there comes the JWKS Endpoint.

JWKS Endpoint is an HTTP Server that responds to GET requests and then returns JWKS (JSON Web Key Set). JWKS is a set of JWKs represented by a JSON object. The JSON object only contains a `keys` member, and the value of `keys` is determined by a JSON array of one or more JWKs.

JWK is a way to store keys in JSON format. A public key in PEM format:

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0CVTPVrufUOfjPvdfzRe
JY9lEknYc0rARYIO2kCDrFvTrQHLwmh11nVmHodxDWJqkzkqRWWoyp5Uy7EG9e/x
y5P4cYtvr+myg1V3RUrYnwvcso0q1LjQSeFVnDH0t1uoCf38aP/jE9xPwNpliqEx
G8gbdoX5xQbk6hox9QOWaNYF0iMJt+As/3BhmgDD0grIzPy/md14KFjxEW8pj5/A
NoGEhsKozHni+yJkxWwgWXb0DLt8XjinpKDbI/e5pcGr6QqCvsH3bstNz8Ke7sft
6tHeKVR2PfcBHYn2fcSeCwN6aOUFhJ30A6T4RIUwbOgX+JGR85d8YUt+28p5leo2
1wIDAQAB
-----END PUBLIC KEY-----
```

If represented as a JWK, it would be of the form:

```
{
  "alg":"RSA256",
  "e":"AQAB",
  "kid":"1",
  "kty":"RSA",
  "n":"0CVTPVrufUOfjPvdfzReJY9lEknYc0rARYIO2kCDrFvTrQHLwmh11nVmHodxDWJqkzkqRWWoyp5Uy7EG9e_xy5P4cYtvr-myg1V3RUrYnwvcso0q1LjQSeFVnDH0t1uoCf38aP_jE9xPwNpliqExG8gbdoX5xQbk6hox9QOWaNYF0iMJt-As_3BhmgDD0grIzPy_md14KFjxEW8pj5_ANoGEhsKozHni-yJkxWwgWXb0DLt8XjinpKDbI_e5pcGr6QqCvsH3bstNz8Ke7sft6tHeKVR2PfcBHYn2fcSeCwN6aOUFhJ30A6T4RIUwbOgX-JGR85d8YUt-28p5leo21w",
  "use":"sig"
}
```

JWK consists of some general fields and algorithm-specific fields, among which common general fields are:

- `kty`: Key Type, indicating the algorithm series used by the current key. the following are three commonly used values:
  - `RSA` indicates that this is a key generated by the RSA algorithm.
  - `EC` indicates that this is a key generated by an ECDSA algorithm.
  - `oct` indicates that this is a symmetric key.
- `use`: Public Key Use, indicating the purpose of the public key. The public key can be used to verify signatures ([JWS](https://www.rfc-editor.org/rfc/rfc7515.html)) or to encrypt data ([JWE](https://datatracker.ietf.org/doc/html/rfc7516)). It has two possible values:
  - `sig`: Verify signature.
  - `enc`: Encrypt data.
- `alg`: Algorithm, indicating the specific algorithm used by the current key, such as RSA256, etc. It must match the `kty`. e.g. `kty` is EC and `alg` is RSA256, then obviously this is a wrong JWT.
- `kid`: Key ID, the unique identifier of the key. When we have multiple keys that can be used to sign the JWT, we can include the kid field in the JWT to indicate which key was used to issue it, so that the verifier can quickly find the key used to verify this JWT. Its value can be any string, so it can be a timestamp, a number, a UUID, or whatever, as long as it helps us distinguish between different keys.

`e` and `n` are the exclusive fields of the RSA algorithm. `e` is the modulus of the RSA public key, and `n` is the exponent of the RSA public key.

The following is an example of returned data from a JWKS Endpoint:

```
{
  "keys":[
    {
      "alg":"RSA256",
      "e":"AQAB",
      "kid":"2",
      "kty":"RSA",
      "n":"vR14JnoiMvqnKuNPLx62vXBPT6OKTK61E9jm-4asIZKbEYwuAKEVCK1r_IYyK0Ok-VuXUwUr5PXbiMZ_S-MN576deJVrIx434NpjacHbL1DXcCpzE600w99hwXk1HlajKZd19XTL9osSOhvzJlyUeeClL0OjXDPT8VfZQIl_w-chvBaQL3gNR3TEzevfXPJ2yHStf-P8w4FRlXv-RQFh1X05don8qqLeWC2iqBhgv1GY_nZttrxL-u6FwLhoP3R8BM2vKY2T1lCtM88sP85q50JdQmHxX8cEZPnuKUuxLVNy3ec9FM-Lv2fzsmEti61aGlkLDKNiXl12EgvNXLz5Iw",
      "use":"sig"
    },
    {
      "alg":"RSA256",
      "e":"AQAB",
      "kid":"1",
      "kty":"RSA",
      "n":"0CVTPVrufUOfjPvdfzReJY9lEknYc0rARYIO2kCDrFvTrQHLwmh11nVmHodxDWJqkzkqRWWoyp5Uy7EG9e_xy5P4cYtvr-myg1V3RUrYnwvcso0q1LjQSeFVnDH0t1uoCf38aP_jE9xPwNpliqExG8gbdoX5xQbk6hox9QOWaNYF0iMJt-As_3BhmgDD0grIzPy_md14KFjxEW8pj5_ANoGEhsKozHni-yJkxWwgWXb0DLt8XjinpKDbI_e5pcGr6QqCvsH3bstNz8Ke7sft6tHeKVR2PfcBHYn2fcSeCwN6aOUFhJ30A6T4RIUwbOgX-JGR85d8YUt-28p5leo21w",
      "use":"sig"
    }
  ]
}
```

## How to build a JWKS Endpoint?

Building a JWKS Endpoint is a straightforward process once you understand its principle.

Taking Python as an example, first, we use the `http.server` module to build a simple HTTP Server, which only supports GET requests.

```
from http.server import HTTPServer, BaseHTTPRequestHandler

HOSTNAME = "127.0.0.1"
PORT = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('{"keys": []}', 'utf-8'))

if __name__ == "__main__":
    web_server = HTTPServer((HOSTNAME, PORT), MyServer)
    print("Server started http://%s:%s" % (HOSTNAME, PORT))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")
```

Next, we only need to implement the code to generate JWKS, and then return it in the callback function `do_GET` of the GET request.

Here we need to use the `jwcrypto` module, so first run the following command to install it:

```
pip3 install jwcrypto
```

We can use the following code to generate a pair of RSA public and private keys:

```
from jwcrypto import jwk

key = jwk.JWK.generate(kty = 'RSA', size = 2048, alg = 'RSA256', use = 'sig', kid = 1)
```

Then export the public or private key in JWK format:

```
# Export Public Key in JWK
key.export(private_key = False)

# Export Private Key in JWK
key.export(private_key = True)
```

The following is the complete code of the JWKS Endpoint example in this article:

```
from jwcrypto import jwk, jwt
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

SAVE_TO = "./private.json"

def issue_jws(key, alg, claims):
    header = {}
    header['alg'] = alg
    header['typ'] = 'JWT'
    header['kid'] = get_kid(key)
    token = jwt.JWT(header = header, claims = claims)
    token.make_signed_token(key)
    return token.serialize()

def generate_jwks(number):
    jwks = []
    for kid0 in range(1, number + 1):
        kid = str(kid0)
        key = jwk.JWK.generate(kty = 'RSA', size = 2048, alg = 'RSA256', use = 'sig', kid = kid)
        jwks.append(key)

    return jwks

def get_kid(key):
    return key.export(private_key = False, as_dict = True).get("kid")

def save_jwks(jwks):
    private_file = open(SAVE_TO, mode = 'w+')
    private_keys = []
    for jwk in jwks:
        private_keys.append(jwk.export(private_key = True, as_dict = True))

    json.dump({"keys": private_keys}, private_file)
    private_file.close()

def load_public_jwks():
    private_file = open(SAVE_TO, mode = 'r')
    jwks = jwk.JWKSet.from_json(private_file.read())
    private_file.close()
    return jwks.export(private_keys = False)

HOSTNAME = "127.0.0.1"
PORT = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(load_public_jwks(), 'utf-8'))

if __name__ == "__main__":
    jwks = generate_jwks(3)

    # Export public key and private key in PEM
    public_key_in_pem = jwks[0].export_to_pem()
    private_key_in_pem = jwks[0].export_to_pem(private_key = True, password = None)

    print("[Public Key]\n%s" % (str(public_key_in_pem, 'utf-8')))
    print("[Private Key]\n%s" % (str(private_key_in_pem, 'utf-8')))

    # Sign the JWT using the first JWK
    claims = {}
    claims['client'] = 'myclient'
    claims['username'] = 'myuser'
    jwt = issue_jws(jwks[0], 'RS256', claims)

    print("[JWT]\n%s\n" % (jwt))

    save_jwks(jwks)
    
    web_server = HTTPServer((HOSTNAME, PORT), MyServer)
    print("Server started http://%s:%s" % (HOSTNAME, PORT))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")
```

In this code, we first use the RSA algorithm to sign three sets of key pairs and then use the private key in the first set of key pairs to sign a JWT.

```
jwks = generate_jwks(3)
...
claims = {}
claims['client'] = 'myclient'
claims['username'] = 'myuser'
jwt = issue_jws(jwks[0], 'RS256', claims)
```

When the program is running, the public key and private key in the first set of key pairs, as well as the issued JWT will be output to the console, where the key will be output in PEM format, we can directly copy them to the [JWT.IO](https://jwt.io/)  tool for verify.

```
[Public Key]
...

[Private Key]
...

[JWT]
...
```

![JWT](https://assets.emqx.com/images/a3a386848ef0ea65a4e2ca4a91e3371c.png)

> In real applications, the private key should always be kept safe, and only the public key is allowed to be disclosed.

Then the private keys in these three sets of key pairs will be saved in the `private.json` in the running directory for reading when the `do_GET` function runs. Because the private key already contains the information of the public key, we only need to save the private key, and there is no need to save the public key and the private key at the same time.

```
save_jwks(jwks)
```

Finally, in the callback function `do_GET` of the GET request, we derive the public key from the private key in the `private.json` and return it in JWKS format:

```
def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(bytes(load_public_jwks(), 'utf-8'))
```

## Verify

Run this code, when the console outputs the following content, it means that the JWKS Endpoint starts successfully:

```
Server started <http://127.0.0.1:8080>
```

Then we can visit `http://127.0.0.1:8080` in the browser, and we will see the following return:

![http://127.0.0.1:8080](https://assets.emqx.com/images/33d132053419821081ef94fb9a47412b.png)

Next, we need to configure a JWT authentication instance using JWKS Endpoint in EMQX.

Let's first start an EMQX instance using Docker:

```
docker pull emqx/emqx:5.1.1
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.1
```

After the startup is successful, we open `http://localhost:18083` in the browser to access the Dashboard, and then enter the authentication page to create a JWT authentication:

![EMQX Dashboard](https://assets.emqx.com/images/4e6f06710be1e77db40b66455985ae9c.png)

Keep other configurations unchanged, configure JWKS Endpoint as `http://127.0.0.1:8080`[,](http://127.0.0.1:8080,/) and click `Create`.

> In this example, EMQX and JWKS Endpoint are deployed on the same machine. You need to adjust the configuration of JWKS Endpoint according to your actual situation.

Next, we open [MQTTX](https://mqttx.app/), create a new connection, copy the JWT output when JWKS Endpoint starts to the Password field, and click `Connect` in the upper right corner to connect.

![MQTTX](https://assets.emqx.com/images/843190605810b6fb9e3d91c6dfe25d2f.png)

We will see that the connection is successfully established. If we make any changes to the currently used JWT, or self-sign a JWT with a different key, we will be denied the connection.

## Conclusion

The above explanation outlines the complete process of deploying a JWKS Endpoint for JWT authentication of EMQX. While this example provides a basic illustration, it encompasses all essential core operations(in real-world scenarios, JWKS Endpoint will not be responsible for key generation). We hope this article will assist you in setting up your own JWKS Endpoint effectively.





<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
