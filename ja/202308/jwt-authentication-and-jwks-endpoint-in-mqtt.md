## はじめに

認証は、[MQTTサービス](https://www.emqx.com/ja/cloud)のセキュリティを確保する上で重要な手段です。[EMQX](https://www.emqx.com/ja/products/emqx)は、パスワード認証、トークンベース認証、拡張認証など、さまざまな認証方法を提供しています。

この記事では、JWT(JSON Web Token)を用いたトークンベース認証の基本原理と、JWKSエンドポイントの構築方法について説明します。

## トークンベース認証とは

EMQXでパスワード認証を利用する場合、クライアントはEMQXによって認証されます。一方、トークンベース認証では、認証サーバーがユーザー名やパスワードをEMQXに露出することなく、アイデンティティの検証を行うことができます。また、認証サーバーから発行されたトークンが有効期限内である限り、再認証する必要がありません。

トークンベース認証のプロセスは以下のようになります。

1. [MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)が、ユーザー名やパスワードなどの資格情報を使用して、認証サーバーに対して認証要求を送信する

2. 認証サーバーは資格情報を検証し、検証にパスした場合にトークンを発行してクライアントに返送する

3. クライアントは、認証サーバーから取得したトークンを使用して、[MQTTサーバー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)に接続要求を送信する

4. MQTTサーバーは、クライアントが持つトークンをチェックし、認証サーバーによって署名され、内容が改ざんされていないことを確認する。チェックにパスした場合、クライアントの接続を許可する

![Token-Based Authentication](https://assets.emqx.com/images/24afb3bb3d6a8936f14c86da166b797d.png)

## JWTベースのトークンベース認証

したがって、トークンベース認証の鍵となるのは、MQTTサーバーがクライアントが持つトークンが認証サーバーによって発行された正規のもので、第三者に偽造されていないことを確認できる必要があることです。また、トークンの内容が改ざんされていないことも検証できる必要があります。

一般的な方法は、JWTをトークンとして利用することです。認証サーバーはJWTの内容に対して署名を適用することで、JWTの整合性と発行元を確認できるようになります。署名の生成方法としては、メッセージ認証コードやデジタル署名が使われますが、セキュリティ上の理由から後者を推奨します。

## メッセージ認証コード(MAC)

メッセージ認証コードの原理は、秘密鍵を用いて入力されたデータのMAC値を計算することです。同じ鍵を用いれば、異なる入力で異なるMAC値が生成されます。また、入力が同じで鍵が異なれば、異なるMAC値が生成されます。

したがって、認証サーバーとMQTTサーバーで鍵を共有できれば、認証サーバーはその鍵を使ってJWTの内容のMACを計算し、それを内容に追加できます。MQTTサーバーは受信したJWTに対して持つ鍵を使って内容のMAC値を計算し、JWTのMAC値と比較することで、メッセージが改ざんされておらず、発行者が正しい鍵を持つことを確認できます。

![Message Authentication Code (MAC)](https://assets.emqx.com/images/21d1ccd02f20235c20a1db19ae703b31.png)

HMAC(ハッシュベースのメッセージ認証コード)は、メッセージ認証コードを構築するために一方向ハッシュ関数を利用する一般的な手法です。HS256、HS384など、使用するSHA関数に基づいて分類されます。

しかし、メッセージ認証コードの欠点も明らかです。鍵をすべてのJWT検証者と共有する必要があるため、鍵の漏洩リスクが高まります。検証者が鍵を持っていれば、JWTを発行することも可能です。したがって、発行者が正しい鍵を持っていることは分かりますが、それが認証サーバーであることを保証することはできません。

## デジタル署名

メッセージ認証コードが抱える課題を考えると、通常はデジタル署名を推奨します。認証サーバーは秘密鍵を使って署名を生成し、MQTTサーバーは公開鍵を使って署名を検証します。公開鍵は誰でも共有可能ですが、署名の検証はできても生成はできません。

したがって、認証サーバーの秘密鍵が漏洩しなければ、有効な署名が付されたJWTは認証サーバーによって発行されたと見なせます。一般的なデジタル署名アルゴリズムには、RSA、ECDSAなどがあります。

## JWTの署名生成

署名は、検証を容易にするためにJWTに直接含められます。JWTはピリオドで区切られたヘッダー、ペイロード、署名の3つの部分から構成されます。署名の対象はヘッダーとペイロード部分になります。

ネットワーク上での伝送を容易にするため、これら3つの部分は最終的にBase64Urlエンコードされます。したがって、一般的に目にするJWTの形式は次のようになります。

```
base64UrlEncode(Header) + "." + base64UrlEncode(Payload) + "." + base64UrlEncode(Signature)
```

## ヘッダー

ヘッダーはJSONオブジェクトで、通常はトークンの種類と使用する署名アルゴリズム(HS256、RS256など)の2つの部分から構成されます。

```
{
  "typ": "JWT",
  "alg": "HS256"
}
```

JWTの署名アルゴリズムの完全なリストは[RFC7518](https://www.rfc-editor.org/rfc/rfc7518)にあります。

## ペイロード

ヘッダーに続くペイロードも、必要なクレームを送信するために使用されるJSONオブジェクトです。JWTの定義済みクレームを使用できます。これらには通常、明確な目的とデータ型があります。例えば、"iat"クレームは現在のトークンの発行時刻を記録し、"exp"クレームは現在のトークンの有効期限を示します。また、任意の名前とデータ型を使用したカスタムクレームも使用できます。

以下の例は、定義済みクレームとカスタムクレームの両方を含んでいます。

```
{
  "name": "John Doe",
  "iat": 1516239022
}
```

## 署名

次に、これまでのヘッダーとペイロードに対して署名を生成し、データ改ざんを防止する必要があります。

HS256を例に取ると、署名の生成方法は次のとおりです。

```
HMACSHA256(base64UrlEncode(Header) + "." + base64UrlEncode(Payload), Secret)
```

[JWT.IO](https://jwt.io/)ツールを使用すると、上記のヘッダーとペイロードに対するJWTを生成できます。HS256アルゴリズムを使用し、鍵を`emqx`と指定すると、次のようなJWTが得られます。

![JWT](https://assets.emqx.com/images/2a78c5e108660261a6ce153ae6749a44.png)

そして、同じヘッダーとペイロードに対する署名を次のPythonコードで計算し、[JWT.IO](https://jwt.io/)によって与えられた署名と比較することができます。

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

以上でJWTの概要とJWTへの署名生成方法が分かりました。署名はJWTの内容を暗号化していないことに注意が必要です。したがって、JWTに機密データを含めることは推奨されません。また、JWTの漏洩を防ぐために、認証サーバーやMQTTサーバーへのクライアント接続はTLSによる暗号化が強く推奨されます。

## JWKSエンドポイントとは

使用する署名アルゴリズムに関わらず、鍵の漏洩リスクが常に存在します。したがって、鍵のローテーションや更新を定期的に行うことが望ましいでしょう。しかし、新しい鍵を手動でサーバーに設定するのは望ましくなく、特に複数のサーバーで同じ鍵セットを使用する場合には非効率的です。マルチテナントのシナリオでは、テナントごとに異なる鍵を提供する必要もあるでしょう。

鍵の管理と配布のために、より効率的なメカニズムが必要不可欠となります。そこで登場するのが、JWKSエンドポイントです。

JWKSエンドポイントは、GETリクエストに応答してJWKS(JSON Web Key Set)を返すHTTPサーバーです。JWKSはJWK(JSON Web Key)の集合をJSONオブジェクトで表現したものです。JSONオブジェクトは`keys`メンバーのみを含み、`keys`の値は1つ以上のJWKのJSON配列で決定されます。

JWKは、鍵をJSON形式で保存するための方式です。PEM形式の公開鍵:

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

これをJWKとして表現すると、次のようになります。

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

JWKは、一般的なフィールドとアルゴリズム固有のフィールドで構成されています。主な一般フィールドは以下の通りです。

- `kty`: 鍵の種類。使用するアルゴリズム系列を示す。主に以下の3つの値が使われる。

  - `RSA`: RSAアルゴリズムによって生成された鍵を示す

  - `EC`: ECDSAアルゴリズムによって生成された鍵を示す

  - `oct`: 対称鍵を示す

- `use`: 公開鍵の用途。公開鍵の目的を示す。次の2つの値が可能。

  - `sig`: 署名の検証

  - `enc`: データの暗号化

- `alg`: アルゴリズム。使用する具体的なアルゴリズムを示す(RSA256など)。`kty`と一致している必要がある。

- `kid`: 鍵ID。鍵の一意の識別子。JWTの署名に使用できる複数の鍵がある場合、そのJWTの発行に使用された鍵を示すために、kidフィールドをJWTに含めることができ、検証側はこのフィールドを使って迅速に鍵を探すことができる。任意の文字列が値として使えるので、タイムスタンプ、番号、UUID等、鍵を区別するのに役立つものであれば何でも良い。

- `e`と`n`はRSAアルゴリズム固有のフィールド。`e`はRSA公開鍵の係数、`n`はRSA公開鍵の指数を示す。

JWKSエンドポイントからのレスポンス例:

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

## JWKSエンドポイントの構築

JWKSエンドポイントの原理が理解できれば、その実装は簡単なプロセスとなります。

Pythonを例に取ると、まず`http.server`モジュールを使用して、GETリクエストのみをサポートするシンプルなHTTPサーバーを構築します。

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

次に、JWKSを生成するコードを実装し、GETリクエストのコールバック関数`do_GET`でこれを返すだけです。

ここでは`jwcrypto`モジュールが必要なので、まず次のコマンドでインストールします。

```
pip3 install jwcrypto
```

次のコードを使用してRSAの公開鍵と秘密鍵のペアを生成できます。

```
from jwcrypto import jwk

key = jwk.JWK.generate(kty = 'RSA', size = 2048, alg = 'RSA256', use = 'sig', kid = 1)
```

そして、公開鍵または秘密鍵をJWKフォーマットでエクスポート:

```
# Export Public Key in JWK
key.export(private_key = False)

# Export Private Key in JWK
key.export(private_key = True)
```

以下は、本記事のJWKSエンドポイントの例の完全なコードです。

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

このコードでは、まずRSAアルゴリズムを使用して3組のキーペアを生成し、最初のキーペアの秘密鍵を使用してJWTに署名しています。

```
jwks = generate_jwks(3)
...
claims = {}
claims['client'] = 'myclient'
claims['username'] = 'myuser'
jwt = issue_jws(jwks[0], 'RS256', claims)
```

プログラムの実行時に、最初のキーペアの公開鍵、秘密鍵、発行されたJWTがコンソールに出力されます。鍵はPEM形式で出力されるため、[JWT.IO](https://jwt.io/)ツールに直接コピーして検証できます。

```
[Public Key]
...

[Private Key]
...

[JWT]
...
```

![JWT](https://assets.emqx.com/images/a3a386848ef0ea65a4e2ca4a91e3371c.png)

> 実際のアプリケーションでは、秘密鍵は常に安全に保管し、公開鍵のみを公開する必要があります。

そして、`do_GET`関数の実行時に、`private.json`内の3組のキーペアの秘密鍵を読み込みます。秘密鍵には公開鍵の情報が含まれているため、公開鍵と秘密鍵の両方を保存する必要はありません。

```
save_jwks(jwks)
```

最後に、GETリクエストのコールバック関数`do_GET`内で、`private.json`の秘密鍵から公開鍵を導出し、JWKS形式で返します。

```
def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(bytes(load_public_jwks(), 'utf-8'))
```

## 検証

このコードを実行すると、次の内容がコンソールに出力された時点で、JWKSエンドポイントが正常に起動したことを意味します。

```
Server started http://127.0.0.1:8080
```

そして、ブラウザで `http://127.0.0.1:8080` にアクセスすると、次のように返ってきます。

![http://127.0.0.1:8080](https://assets.emqx.com/images/33d132053419821081ef94fb9a47412b.png)

次に、JWKSエンドポイントを使用するJWT認証インスタンスをEMQXに設定する必要があります。

まず、Dockerを使用してEMQXインスタンスを起動します。

```
docker pull emqx/emqx:5.1.1 
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.1.1
```

起動後、ブラウザで `http://localhost:18083` にアクセスしてダッシュボードに入り、認証ページでJWT認証を作成します。

![EMQX Dashboard](https://assets.emqx.com/images/4e6f06710be1e77db40b66455985ae9c.png)

他の設定は変更せずに、JWKSエンドポイントを `http://127.0.0.1:8080` に設定し、[作成]をクリックします。

> この例では、EMQXとJWKSエンドポイントが同じマシンにデプロイされています。実際の状況に応じてJWKSエンドポイントの設定を調整する必要があります。

次に、[MQTTX](https://mqttx.app/ja)を開き、新しい接続を作成し、JWKSエンドポイント起動時に出力されたJWTをパスワードフィールドにコピーし、右上の[`接続`]をクリックして接続します。

![MQTTX](https://assets.emqx.com/images/843190605810b6fb9e3d91c6dfe25d2f.png)

接続が正常に確立されたことを確認できます。現在使用しているJWTを変更したり、異なる鍵でJWTに自己署名した場合は、接続が拒否されます。

## まとめ

以上で、EMQXのJWT認証のためのJWKSエンドポイントの導入プロセスの概要を説明しました。この例は基本的な説明を提供していますが、実際のシナリオでは鍵の生成はJWKSエンドポイントの責任ではありません。本記事が、効果的に独自のJWKSエンドポイントを設定するのに役立つことを願っています。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
