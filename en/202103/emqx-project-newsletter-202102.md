Hello! Things are moving fast. Thanks to a great community & fantastic dedicated EMQX open-source team, we are developing features & fixes at a break neck pace.

February was a hotpot of cutting edge protocol support, community engagement, security and more features. Here’s what we have been up to.



## Live Feature show case Session

We had our first informal live demo session ( via Zoom ). It was a packed house with multiple teams & community members joining. 

A community contribution was demonstrated and well received by everyone, which also included insights on specific customer use cases. 

The open source team show cased the new environment variable config overriding & the MsQuic proof of concept. The new Env overriding provides great flexibility, just a little taste of the greater configuration enhancements taking place.

The MsQuic PoC speaks to our commitment to lead in the market. Enabling customers to stay cutting edge in competitive industries.

Thank you to our presenters from the EMQX open source team, community contributors and all the attendees, for an informative event with great energy.

We hope to have many more.



## Security

#### TLS v1.3 as default

From OTP 23 we have set TLS 1.3 as default. Selecting the best security first while still being able to support earlier versions when needed.



## Environment Variable config overrides

#### Flexibility 

General configuration can be overridden using environment variables, useful for testing and non persistent use cases.



## Master branch leads Repo

#### Latest Features 

The master branch is now the cutting edge, try out the latest features as they are pushed. Releases will be tagged from master and maintenance branches created from releases.



## QUIC Protocol in the works

#### Staying ahead of the curve

A NIF (Erlang Native Implemented Functions) based QUIC ( [MsQuic](https://github.com/microsoft/msquic) from Microsoft ) PoC developed & demonstrated. Paving the way to road mapping QUIC support in future. Please follow up on [emqx/quic](https://github.com/emqx/quic) for latest updates.



## Enterprise features to Open Source 

#### Supporting the community with more functionality. 

- Webhook & MQTT bridge plugin now have the certificate upload feature Open sourced for the community. We’re sure this feature is a welcomed sight to the open source community.
- Wolff is has been disclosed ( [kafka4beam/wolff](https://github.com/kafka4beam/wolff) ) 

How is it different from brod?

- More resilient to network and Kafka disturbances
- More flexible connection management
- Auto partition count refresh



## V4.3 Beta

#### Now Finalizing

The team are delivering great sprints from our product managers, bringing the anticipated v4.3 Beta tantalizingly close. 

## Exhook Benchmark

#### reaches 20k/s TPS on 8 core CPU, 16 GB RAM

Exhook ( emqx-exhook ) is a plugin in emqx. It’s main objective is forwarding all hook events via grpc to servers implemented in another language, greatly improving the extensibility of emqx. The recent benchmark achieved 20k/s TPS on 8 core CPU, 16 GB RAM.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
