>**Summary:** On 18 and 19 October 2026, sixteen intermediate certificates were revoked for the reason `ca_compromise` after the private keys of four eMudhra root certificates were exposed. Two of the four affected roots were present in EMQX Enterprise Docker images. This page is a short summary; the authoritative details, certificate hashes, and verification procedures are in our security advisory: [**GHSA-qxwr-jcff-c3wm — Remove the compromised eMudhra root certificates without upgrading**](https://github.com/emqx/emqx/security/advisories/GHSA-qxwr-jcff-c3wm)

## What Happened



This is not a defect in EMQX code. No input to EMQX triggers it, and no EMQX configuration makes it reachable. What changed is the trustworthiness of certificates that ship inside our Docker images.

An EMQX Docker image carries two separate certificate authority trust stores:

| Trust store                                                  | Who reads it                                                 |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| The `certifi` bundle compiled into the release               | EMQX components that make outgoing HTTPS calls through `hackney` |
| The operating system bundle at `/etc/ssl/certs/ca-certificates.crt` | The `curl` and `openssl` binaries in the image, not EMQX itself |

Both contained withdrawn roots. We checked every supported release line and verified each certificate by SHA-256 rather than by name, because several sibling certificates have very similar names and are not part of this incident.

## What it Means for Your Deployment



The exposure is narrow, and we want to be precise about it rather than alarming.

**Not Affected:**

- **MQTT & Dashboard listeners**: Incoming connections and management access remain secure.
- **Database Connectors**: Kafka, PostgreSQL, MySQL, MongoDB, and other database integrations.
- **Clients**: Clients connecting to EMQX are completely unaffected. There is no path to code execution and no new external attack vector into a node.

**Affected Components:**

Outgoing HTTPS calls from components using the bundled trust store when no custom CA certificate file is configured.

- AI Completion
- HTTP Authentication and Authorization
- S3 and S3 Tables actions
- A small number of connectors that do not currently expose a TLS setting of their own

To use any of this, someone would already need to hold a certificate issued under the exposed keys *and* to sit on the network path between your node and the service which EMQX is configured to call. EMQX gives them neither. The advisory rates this Moderate, and explains in detail why the 5.8, 5.9 and 5.10 lines are the harder case: the `certifi` bundle on those lines also contains a root that directly issued eight of the sixteen revoked intermediates.

## What We Have Done



- **Audited every supported release line and both trust stores**, and verified the contents by certificate hash against the image contents rather than by reading a manifest.
- **Re-published the 6.3.2 image on 22 October 2026** from a freshly pulled base image. Its operating system bundle now contains none of the four withdrawn roots.
- **Published a replacement** `certifi` **module for every supported line** at [emqx/emqx-hot-patches](https://github.com/emqx/emqx-hot-patches), each with its SHA-256 so you can check what you install, and each built against the certifi version that line actually ships.
- **Published the advisory with verification commands**, so you can confirm the condition on your own nodes before and after the change instead of taking our table on trust.
- **Documented the limits honestly**, including the components that do not yet accept a CA certificate file of their own, and what to do about them in the meantime.

## What Comes Next: A Proper Fix in Every Line



The manual procedure in the advisory exists so that you are not blocked while waiting for a release. You will not have to keep it.

**The next patch release in every supported line will carry the corrected trust store. After you upgrade, no manual patching is required.**

| Release line | Fixed in |
| :----------- | :------- |
| 5.8          | 5.8.12   |
| 5.9          | 5.9.4    |
| 5.10         | 5.10.6   |
| 6.0          | 6.0.5    |
| 6.1          | 6.1.6    |
| 6.2          | 6.2.4    |
| 6.3          | 6.3.3    |

One step matters if you apply the manual procedure first. EMQX puts the patches directory ahead of the release in its code path, and an upgrade does not clear that directory. **Delete the patched module from the patches directory before you upgrade, then restart the node.** A module left behind keeps overriding the one in the new release.

We are also extending explicit CA certificate configuration to the outgoing HTTPS components that do not yet offer it. Setting your own trust anchors is the right configuration independently of this incident, and it should be available everywhere it makes sense.

## Why We Are Publishing This



A withdrawn root certificate in a shipped image is the kind of thing that is easy to leave unsaid. The exposure here is narrow, the conditions are demanding, and no EMQX code is at fault.

We would rather tell you transparently, provide the hashes and commands, and empower you to verify your own deployment.

If you have questions, or evidence of a certificate issued under these keys, please write to [security@emqx.io](mailto:security@emqx.io).

## References

- [eMudhra Intermediate CA Compromise](https://emudhra.we-have-a-problem.com/) — the public tracker for the incident. It records how the key compromise was demonstrated, what each root programme has done and when, and it includes a browser check that tells you whether your own client still trusts the affected intermediates.
- [GHSA-qxwr-jcff-c3wm](https://github.com/emqx/emqx/security/advisories/GHSA-qxwr-jcff-c3wm) — the EMQX security advisory, with the certificate hashes, the per-image findings and the full procedure.
- [emqx/emqx-hot-patches](https://github.com/emqx/emqx-hot-patches) — the replacement modules, their checksums and the rules for using a patches directory.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
