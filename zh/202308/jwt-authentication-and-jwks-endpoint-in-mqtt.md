[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 的认证机制是保障 MQTT 服务安全性的重要手段。[EMQX](https://www.emqx.com/zh/products/emqx) 提供了密码认证、Token 认证以及增强认证等多种认证手段供用户选择。本文将介绍基于 JWT（JSON Web Token，一种定义了如何在网络应用间传递 JSON 对象的开放标准） 的 Token 认证的基本原理，以及如何使用 EMQX 构建我们自己的 JWKS Endpoint。

## 什么是 Token 认证？

当我们在 EMQX 中使用密码认证时，对客户端的身份验证工作将由 EMQX 来完成。而 Token 认证允许我们将身份验证工作交给独立的认证服务器来完成，而不必将用户名和密码暴露给 EMQX，并且在认证服务器授予的 Token 过期前不需要重复认证。

它的完整过程可以概括为以下四步：

1. 客户端首先携带用户名、密码等用户凭据向认证服务器发起认证请求。
2. 认证服务器对客户端持有的用户凭据进行验证，验证通过后签发一个 Token 返回给客户端。
3. 客户端使用认证服务器授予的 Token 向 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)发起连接请求。
4. MQTT 服务器会对客户端持有的 Token 进行检查，确认它是否由认证服务器签发，以及内容是否被篡改。检查通过后客户端将被允许连接。

![Token-Based Authentication](https://assets.emqx.com/images/24afb3bb3d6a8936f14c86da166b797d.png)

## 基于 JWT 的 Token 认证

所以 Token 认证的关键点在于，MQTT 服务器既要能够确认客户端持有的 Token 是由认证服务器签发的，而不是第三方伪造的，也要能够确认 Token 的内容没有被篡改。

一个常见的办法就是使用 JWT 作为 Token，我们可以让认证服务器为 JWT 的内容施加一个签名，以便检查 JWT 的完整性和来源。常见的生成签名的方式有消息认证码与数字签名，但出于安全性的考量，我们一般更推荐使用后者。

### 消息认证码

消息认证码的原理是使用一个密钥对给定的输入计算 MAC 值。相同的密钥，输入不同，MAC 值就会不同。而相同的输入，密钥不同，MAC 值也会不同。

所以我们可以让认证服务器和 MQTT 服务器共享一个密钥，认证服务器使用这个密钥为 JWT 的内容计算 MAC，然后追加到内容之后。MQTT 服务器在收到这个 JWT 后，同样使用自己持有的密钥计算内容的 MAC 值，然后与 JWT 中的 MAC 值进行比较，如果两者一致，则说明消息没有篡改，并且签发者持有正确的密钥。

![Message Authentication Code (MAC)](https://assets.emqx.com/images/21d1ccd02f20235c20a1db19ae703b31.png)

HMAC(Hash-Baed Message Authentication Code) 就是一种常用的使用单向散列函数来构造消息认证码的方法，根据使用的 SHA 函数的不同，又分为 HS256、HS384 等等。

但是消息认证码的缺点也很明显，那就是我们必须将密钥共享给所有 JWT 的验证方，这增加了密钥泄漏的风险。而且一旦验证方持有了密钥，那么其实它也有了签发 JWT 的能力。所以我们只能知道签发者持有正确的密钥，却不能保证它一定是认证服务器。

### 数字签名

鉴于消息认证码中存在的问题，通常我们更推荐使用数字签名，认证服务器使用私钥生成签名，MQTT 服务器使用公钥来验证签名。我们可以把公钥分享给任何人，但他们都只会有验证签名的能力，而不会有生成签名的能力。只要认证服务器持有的私钥没有泄漏，我们就可以认为拥有合法签名的 JWT 一定是认证服务器签发的。常见的数字签名算法有 RSA、ECDSA 等。

## 为 JWT 施加签名

为了方便对端验证，签名会直接包含在 JWT 中。JWT 被 . 分隔成三个部分，它们分别是 Header、Payload 和 Signature。我们签名的对象正是其中的 Header 与 Payload 部分。

为了让 JWT 能够更好地在网络中传输，这三个部分最终都会被 Base64Url 编码。所以通常我们看到的 JWT 都是这样的：

```
base64UrlEncode(Header) + "." + base64UrlEncode(Payload) + "." + base64UrlEncode(Signature)
```

### Header

最前面的 Header 是一个 JSON 对象，它通常由两部分组成：令牌的类型和所使用的签名算法，例如 HS256、RS256 等等。

```
{
  "typ": "JWT",
  "alg": "HS256"
}
```

完整的 JWT 签名算法列表可以查询 [RFC7518](https://www.rfc-editor.org/rfc/rfc7518)。

### Payload

紧随 Header 之后的 Payload 同样也是一个 JSON 对象，用来携带我们需要传递的各种声明。我们可以使用 JWT 预定义的声明，它们一般有着确定的用途和数据类型。例如 iat 声明用于记录当前 Token 的签发时间，exp 声明用于指示当前 Token 的过期时间。我们也可以使用自定义的声明，它们可以使用任意的名称和数据类型。

以下示例包含一个预定义声明和一个自定义声明：

```
{
  "name": "John Doe",
  "iat": 1516239022
}
```

### Signature

现在，我们需要为前面的 Header 和 Payload 的施加一个签名，防止数据篡改。

以 HS256 为例，生成签名的方式如下：

```
HMACSHA256(base64UrlEncode(Header) + "." + base64UrlEncode(Payload), Secret)
```

我们可以使用 [http://jwt.io](http://jwt.io) 工具来为以上内容生成一个 JWT。当我们使用 HS256 算法，并指定密钥为 emqx 时，我们将得到以下 JWT：

![JWT](https://assets.emqx.com/images/2a78c5e108660261a6ce153ae6749a44.png)

然后我们可以使用以下 Python 代码为相同的 Header 和 Payload 计算签名并与 [http://jwt.io](http://jwt.io) 给出的签名进行比较：

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

现在我们知道了什么是 JWT，以及如何为 JWT 生成签名。但我们需要注意，签名并不会加密 JWT 的内容，这也是我们不建议你在 JWT 中携带敏感数据的原因。另外，为了防止 JWT 泄漏，我们建议客户端与认证服务器、MQTT 服务器的连接均使用 TLS 加密。

## 什么是 JWKS Endpoint

无论我们使用哪种签名算法，都存在密钥泄漏的风险。所以为了提高安全性，我们通常建议定期轮换或者更新密钥。但显然手动将新的密钥配置到服务器中并不是一个好的选择，特别是多个服务器在使用同一组密钥时。在多租户的场景下，我们可能还需要为不同的租户提供不同的密钥。

所以我们需要一种更加高效的管理和分发密钥的机制，而这就是 JWKS Endpoint 存在的目的。

JWKS Endpoint 本质上就是一个 HTTP Server，它响应 GET 请求，然后返回 JWKS（Json Web Key Set），JWKS 是用一个 JSON 对象表示的一组 JWK，该 JSON 对象只包含一个 keys 成员，keys 的值是由一个或多个 JWK 组成的 JSON 数组。

JWK 是一种以 JSON 格式来存储密钥的方法。一个 PEM 格式的公钥：

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

如果以 JWK 来表示，它将是以下形式：

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

JWK 由一些通用字段和特定于算法的字段组成，其中常见的通用字段有：

- kty：Key Type，指示当前密钥使用的算法系列，以下是三个常用的值：

  - RSA，表示这是一个 RSA 算法生成的密钥。

  - EC，表示这是一个 ECDSA 算法生成的密钥。

  - oct，表示这是一个对称密钥。

- use：Public Key Use，指示公钥的用途，公钥可以用来验证签名（[JWS](https://www.rfc-editor.org/rfc/rfc7515.html)），也可以用来加密数据（[JWE](https://datatracker.ietf.org/doc/html/rfc7516)）。它有两个可取值：

  - sig：验证签名。

  - enc：加密数据。

- alg：Algorithm，指示当前密钥使用的具体算法，例如 RSA256 等。它必须与 kty 相匹配，比如 kty 为 EC，而 alg 为 RSA256，那么显然这是一个错误的 JWT。

- kid：Key ID，密钥的唯一标识符。当我们有多个密钥可用于签署 JWT 时，我们可以在 JWT 中包含 kid 字段来指示签发它时使用的密钥，以便验证方快速地找到验证此 JWT 所需的密钥。它的值可以是任意的字符串，所以它可以是时间戳、数字、UUID 等等，只要它可以帮助我们区分不同的密钥。

e，n 则是 RSA 算法的专属字段，e 是 RSA 公钥的模数，n 是 RSA 公钥的指数。

以下是一个 JWKS Endpoint 的返回数据示例：

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

## 如何构建一个 JWKS Endpoint？

在知道了 JWKS Endpoint 的原理之后，构建它就非常简单了。

以 Python 为例，首先，我们使用 `http.server` 模块构建一个简单的 HTTP Server，它仅支持 GET 请求。

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

接下来，我们只需要实现生成 JWKS 的代码，然后在 GET 请求的回调函数 do_GET 中返回即可。

这里我们需要用到 `jwcrypto` 模块，所以先运行以下命令来安装它：

```
pip3 install jwcrypto
```

我们可以使用以下代码生成一对 RSA 的公私钥：

```
from jwcrypto import jwk

key = jwk.JWK.generate(kty = 'RSA', size = 2048, alg = 'RSA256', use = 'sig', kid = 1)
```

然后以 JWK 格式导出公钥或者私钥：

```
# Export Public Key in JWK
key.export(private_key = False)

# Export Private Key in JWK
key.export(private_key = True)
```

以下为本文 JWKS Endpoint 示例的完整代码：

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

在这段代码中，我们首先使用 RSA 算法签发了三组密钥对，然后使用第一组密钥对中的私钥签发了一个 JWT。

```
jwks = generate_jwks(3)
...
claims = {}
claims['client'] = 'myclient'
claims['username'] = 'myuser'
jwt = issue_jws(jwks[0], 'RS256', claims)
```

程序运行时，第一组密钥对中的公钥和私钥，以及签发的 JWT 都会输出到控制台，其中密钥将以 PEM 格式输出，我们可以直接将它们复制到 [http://jwt.io](http://jwt.io) 工具中进行验证。

```
[Public Key]
...

[Private Key]
...

[JWT]
...
```

![JWT](https://assets.emqx.com/images/a3a386848ef0ea65a4e2ca4a91e3371c.png)

> 在真实的应用中，私钥应当始终被妥善保管，允许对外公开的只有公钥。

然后这三组密钥对中的私钥都会被保存运行目录下的 private.json 文件中，供 do_GET 函数运行时读取。因为私钥已经包含了公钥的信息，所以我们只要保存私钥即可，无需同时保存公钥与私钥。

```
save_jwks(jwks)
```

最后在 GET 请求的回调函数 `do_GET` 中，我们根据 `private.json` 文件中的私钥推导出公钥，并以 JWKS 格式返回：

```
def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(bytes(load_public_jwks(), 'utf-8'))
```

## 验证

运行这段代码，当控制台输出以下内容，说明 JWKS Endpoint 启动成功：

```
Server started <http://127.0.0.1:8080>
```

这时我们在浏览器中访问 `http://127.0.0.1:8080`，将看到以下返回：

![http://127.0.0.1:8080](https://assets.emqx.com/images/33d132053419821081ef94fb9a47412b.png)

接下来，我们需要在 EMQX 中配置一个使用 JWKS Endpoint 的 JWT 认证。

我们先以 Docker 方式启动一个 EMQX 实例：

```
docker pull emqx/emqx:5.1.1
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.1
```

启动成功后我们就可以在浏览器中打开 `http://localhost:18083` 以访问 Dashboard，然后进入到认证页面创建一个 JWT 认证：

![EMQX Dashboard](https://assets.emqx.com/images/4e6f06710be1e77db40b66455985ae9c.png)

保持其他配置不变，将 JWKS Endpoint 配置为 `http://127.0.0.1:8080`，然后点击 Create。

> 本示例中 EMQX 与 JWKS Endpoint 部署在同一台机器中。你需要根据自己的实际情况调整 JWKS Endpoint 的配置。

接下来我们打开 [MQTTX](https://mqttx.app/zh)，新建一个连接，将 JWKS Endpoint 启动时输出的 JWT 复制到 Password 字段中，然后点击右上角的 Connect 进行连接。

![MQTTX](https://assets.emqx.com/images/843190605810b6fb9e3d91c6dfe25d2f.png)

我们将看到连接成功建立，而如果对当前使用的 JWT 做出任何更改，又或者使用其他的密钥自行签发一个 JWT，都将被拒绝连接。

## 结语

以上就是为 EMQX 的 JWT 认证部署一个 JWKS Endpoint 的全部过程。虽然这只是一个最简单的示例，并且我们简化了 JWKS 的管理（在实际的应用中，JWKS Endpoint 并不会负责公私钥的生成），但这已经覆盖了所有必须的核心操作。希望这篇文章可以为您部署自己的 JWKS Endpoint 带来一些帮助。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
