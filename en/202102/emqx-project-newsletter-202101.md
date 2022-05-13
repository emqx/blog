Hello! This is our very first newsletter to share what’s happening in EMQX open-source team.

In January, EMQ open-source work group discussed the plans for 2021. Aiming to improve contribution experience and increase work transparency, in the coming weeks, the open-source work group will define and publish contribution guidelines, as well as a process for proposing major changes to EMQX.
We are looking forward to seeing more contributors around the world join our community in 2021!

- Project updates
  - We released two bug fix versions for the 4.2 series, 4.2.6 and 4.2.7
  - We have released 4.3-alpha.1
    - We are on OTP 23!
    - The emqx Erlang project has been refactored into an umbrella project (or a mono-repo if you will), aiming to free us from dependency hell (from almost 30 different small dependency repos)
    - CI checks are all merged into one place! The benefit of this change is likely not visible immediately and is perhaps hard to grasp without getting into too many details, but here is a try:
      - No more scattered test results, only one link to a list of tests triggered in Github Actions
      - No more questioning about dependency integrity when we had to reverse the dependency for the integration test.
    - Multi-language support, the underlying erlport implementation for exhook and exporto have been replaced by gRPC
    - A lot of smaller enhancements and bug fixes. Stay tuned for the release note.
  - Although the 5.0 scope is yet to be defined, we have managed to kick off some of the new feature developments
    - A brand new configuration management and yet maximized backward compatibility.
    - Async Mnesia transaction replication PoC, aiming to solve large cluster’s brain-split.
- Community updates
  - In January, four new members from EMQ joined oasis-open MQTT-TC. We are looking forward to being more active in the MQTT & MQTT-SN standardization processes.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
