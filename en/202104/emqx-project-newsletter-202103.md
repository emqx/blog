In March, the focus of our work was on finalising 4.3 release as well as the design of EMQ X Broker 5.0. After three weeks of discussions (marathon meetings), we finally compiled a list of requirements for 5.0. This is exciting news, development of 5.0 is about to start.

## 4.3.0 coming soon

We have released 4.3-beta.1, 4.3-rc.1, 4.3-rc.2, 4.3-rc.3, 4.3.0 is coming soon, stay tuned.

## Security

In March, EMQ open-source team has got in touch with Synopsys Software Integrity Group to seek cooperation so we can provide better security in our products and services.

## Community

- In order to make our open source projects more innovative, active, iterative and efficient, the EMQ X team began to formally adopt the RFC process to collect ideas from the community and continue to improve product functions. We named the repository that manages this process EIP ( **EMQ X Improvement Proposals**  [emqx/eip](https://github.com/emqx/eip)).
- We launched the [askemq.com](https://askemq.com/) community this month, which helps users in mainland China to collaborate and share more conveniently.
- This spring in China, we kicked off our campus recruitment with a newly shot a promotional video. Looking forward to more young talent joining us.
- The online demo conference is continuing to be conducted bi-weekly, supported by multiple development teams and community members.
- The EMQ X team is about to hold the first offline open day event in the Hangzhou office.

## Projects

- A dedicated test team is going to help us setup even more automated integration tests in  GitHub CI.
- Our main Erlang project [emqx/emqx.git](https://github.com/emqx/emqx) is now passing dialyzer checks for the entire code base.
- [Quicer](https://github.com/emqx/quic) (the QUIC protocol binding for Erlang/Elixir) project now supports macOS; and more inet/gen_tcp style APIs are added. We are finally about to start the PoC project MQTT-on-QUIC.
- Kicked off the Rlog project aiming to make EMQ X cluster more scalable. Rlog, implemented as a part of the [ekka](https://github.com/emqx/ekka) library, will provide a mechanism to asynchronously replicate Mnesia database. See [EIP-0004](https://github.com/emqx/eip/blob/main/active/0004-async-mnesia-change-log-replication.md) for more details.
- jq.erl. [jq](https://stedolan.github.io/jq/), de-facto JSON processing standard. Based on the open-source core, we have built a NIF binding which will then be integrated into EMQ X's rule engine as a data processing function.
