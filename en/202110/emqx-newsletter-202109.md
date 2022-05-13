Early September, a few of us in the team got invited by the guys from Industry 4.0 Solutions to the Company Spotlight online event. Industry 4.0 Solutions is specialised in digitalising physical factory via the use of Big Data, Cloud platform, Artificial Intelligence (AI) and Industrial Internet of Things (IIoT). At the very center of the IIoT solutions, there is the MQTT broker (cluster), and EMQX is the perfect MQTT broker in this big picture.

It was a great pleasure to meet the people from the IIoT community. During the 1 hour session we had the chance to answer a lot of the burning questions about EMQ as a company and EMQX the MQTT messaging broker as the product. Please check it out in this recording: [https://www.youtube.com/watch?v=nP7JAlpyvfo](https://www.youtube.com/watch?v=nP7JAlpyvfo)

## EMQX v5.0-beta.1 is released

We are excited and proud to announce the first pre-release of EMQX version 5.0. 

Here is a summary of  the features added:

- Unified authentication, authorisation and gateway management
- Unified data-bridge and rule-engine features
- New configuration management (HOCON)
- Async database replication (Mria) to make the cluster even more scalable
- MQTT over QUIC – a bleeding-edge research project 

Please find more details in [the release note](https://github.com/emqx/emqx/discussions/5864).

The new features introduced in 5.0 are now publicly available to experiment and evaluate.
As there are more beta versions to come, the is the perfect timing to express your expectations, requirements and maybe event influence the design of the product.

## More to come in the next beta

In beta.2 release, we’ll focus on bringing the dashboard (which is hidden in beta.1) to the front stage. And even more features which do not involve a lot of user-interface changes.

### Overload protection

When under high load, an “ideal robust system” should automatically start back-pressing to where the load is generated, instead of lowering the quality of service or even crash down. With the overload protection, EMQX will do better than setting a hard limit on the total number of connections etc to protect itself, getting one step closer to the “ideal robust system”.

### Plugin drop-in installation

EMQX is highly extensible, as we wrote in a [blog post](https://www.emqx.com/en/blog/develop-and-deploy-emqx-plugin-for-enterprise-4-3), it is possible for plugins to be installed independently.

Starting from 5.0, EMQX open source users will be able to drop-in install an extension package to upgrade to Enterprise.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
