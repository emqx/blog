In April, EMQX 4.3-beta.5 release summed up all the fixes has to be done before 4.3.0 release. This allowed us to gradually shift our focuses towards 5.0 development. Big thank you to issue reporters and contributors.

## 4.3.0 finalised, with a performance boost

4.3.0 release has been a bit overdue, mainly because we have managed to address some performance issues, the fixes for which are absolutely worth waiting for! Please join our [online demo session](https://github.com/emqx/emqx/discussions/4463) to learn more details in how we managed to make wildcard subscription 10x faster.

## Smooth upgrade

We have released two bug fixes, 4.0.13 and 4.2.11, which fix some problems with data import and export, to ensure smooth data migration when upgrading to 4.3.

## Quality

We are adding more and more automated integration tests, for example PostgreSQL, MySQL, Redis and more

## Flexibility

For Mnesia data sync performance optimisations, we have forked [Erlang/OTP](https://github.com/emqx/otp). We also added a patch to allow atuto-probing network peer’s IPv6 stack support. All the changes are compatible to upstream, meaning EMQX can run on upstream Erlang/OTP without any problem.

## Connectivity (MQTT over QUIC)

We have reached a [new milestone ](https://www.youtube.com/watch?v=j85mDP97MWA)of MQTT-over-QUIC project: Full integration demo of QUIC running inside EMQX. Our next steps are to make it production ready. See project timeline in [this GitHub discussion](https://github.com/emqx/emqx/discussions/4379)

## Scalability (Rlog)

New Rlog achievements demoed, (ref: [video recording](https://www.youtube.com/watch?v=p2P_mC97ciU), and [previous updates](https://github.com/emqx/emqx/discussions/4463)), EMQX nodes now can sync routing information asynchronously! This will make EMQX cluster more stable, scalable and cloud-native.

## Next generation (5.0 features)

[jq](https://stedolan.github.io/jq/), the de facto standard for JSON processing, we have built a NIF binding based on its open source kernel. It can be applied to the EMQX rule engine to provide flexible and powerful extensions for JSON data stream processing. See more details in the [PoC demo recording](https://www.youtube.com/watch?v=V1ceaQNcsEU)

[HOCON](https://github.com/emqx/hocon) will be the next-generation configuration for EMQX. Now we are adding schema support for HOCON. The schema will be use for both config file parsing, and also for config change REST API validation in 5.0 

## Community

We have been doing 3 tracks of open-source events. The events are held offline and online at the same time. Future events will be are scheduled in [this calendar ](https://outlook.office365.com/calendar/published/be323b3a50ea4daeb04bf0c05ed94582@emqx.io/e4ef6b54cc7646ef86574323062cfdce15654452582260728863/calendar.html). Recordings are shared in our[ YouTube channel](https://www.youtube.com/channel/UC5FjR77ErAxvZENEWzQaO5Q).

- Demo Day. After each sprint, we present our achievements in the past tow to three weeks, so users/developers in the community can follow up closely with EMQX development. Please find the details about pas and future demos here in this [GitHub Discussion thread](https://github.com/emqx/emqx/discussions/4463).
- Sharing Day. From time to time, we do knowledge sharing presentations within the teams. Community developers and users are also welcome to join. Sharing is caring, and open-source is all abut sharing, learn and succeed together are our initial and final goal.
- Open Day. From time to time, we invite users/developers to share our and their ideas in how to improve EMQX. Such as new features, long term evolution plans etc.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
