[EMQX Enterprise](https://www.emqx.com/en/products/emqx) version 4.4.18 has been officially released! This release includes support for the OCPP 1.6-J protocol, which enables the communication between Electric Vehicle Supply Equipment to EMQX. This release also brings several enhancements and bug fixes.

## OCPP 1.6-J Support

OCPP-J (Open Charge Point Protocol - JSON) is a protocol for communication between Electric Vehicle Supply Equipment (EVSE) and Electric Vehicle Management Systems (EVMS). OCPP-J is based on JSON (JavaScript Object Notation) and is a lightweight and flexible protocol that is easy to implement and integrate with other systems.

With the implementation of the emqx_ocpp plugin based on the OCPP 1.6-J standard, EMQX Enterprise offers seamless integration with Charge Point devices. This plugin handles formatting conversion, and forwarding of upstream and downstream messages, acting as an OCPP gateway for EMQX. It enables protocol transfer between OCPP and MQTT, allowing charging stations to connect easily to EMQX through OCPP over WebSocket. 

![Seamless integration with Charge Point devices](https://assets.emqx.com/images/903e5af0c4edba8ddeeef27666eabaaa.png)

By supporting OCPP 1.6-J, EMQX Enterprise significantly improves its functionality and efficiency, providing a powerful device access and data integration capability for Electric Vehicle charging management.

## Enhancements and Bug Fix

- Improved the placeholder syntax of the rule engine.

  The parameters of actions support using placeholder syntax to dynamically fill in the content of strings. The format of the placeholder syntax is `${key}`. Before this improvement, the `key` in `${key}` could only contain letters, numbers, and underscores. Now the `key` supports any UTF8 characters.

- Fixed the issue where required plugins were missing in `data/load_plugins`.

  Before this fix, if the `data/load_plugins` file was manually deleted and EMQX was restarted, three required plugins (`emqx_schema_registry`, `emqx_eviction_agent`, `emqx_node_rebalance`) would not be automatically enabled and would not be recorded in the newly generated `data/load_plugins` file.

## Summary

The OCPP 1.6-J support in EMQX Enterprise is a significant step forward for the Electric Vehicle Charging industry, helping to improve the management and efficiency of charging operations and facilitating the integration of EVSEs with other IoT devices and systems. We encourage all users to download EMQX Enterprise 4.4.18 to use these new features.

Contact EMQX Enterprise support for any questions or assistance: [Contact Us →](https://www.emqx.com/en/contact?product=emqx)



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
