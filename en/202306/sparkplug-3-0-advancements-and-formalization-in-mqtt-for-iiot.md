The release of Sparkplug 3.0 brings significant advancements and formalization to the [MQTT Sparkplug](https://www.emqx.com/en/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0) protocol for Industrial Internet of Things ([IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges)) applications. Developed by the Eclipse Sparkplug Working Group, this new version aims to clarify ambiguities present in the previous 2.2 specifications while maintaining the overall intent of the v2.2 specification.

## **Key Enhancements in Sparkplug 3.0**

### Clearer Specification Structure

The new specification replaces the "Background" chapter of the v2.2 specification with the "Principles" chapter. This section provides a detailed description of the fundamental principles underlying Sparkplug. Additionally, the "Operational Behavior" chapter extensively covers the operational aspects of the Sparkplug environment.

### Targeted Clarity and Formality

The primary objective of Sparkplug 3.0 is to provide clear and formal specifications, addressing any ambiguities present in the previous version. By doing so, it aims to establish explicit normative statements for the protocol, ensuring consistency and ease of implementation.

### Incorporation of MQTT 5.0 Specifics

Sparkplug 3.0 includes specific settings related to MQTT 5.0, particularly addressing different session settings like "Clean Start" in MQTT 5.0 compared to "[Clean Session](https://www.emqx.com/en/blog/mqtt-session)" in MQTT 3.1.1. These additions align Sparkplug with the enhancements introduced in MQTT 5.0.

### Subset Requirements for MQTT Servers

Sparkplug infrastructure has a specific subset of requirements for [MQTT servers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison). Any MQTT 3.1.1 server or broker that adheres to the complete specification will meet the requirements of the Sparkplug infrastructure.

As for MQTT server, it is clearly defined into two requirement levels in the Sparkplug specification. The first level is that as long as the MQTT server meets MQTT 3.1.1, it generally meets these requirements. The second level requires additional capabilities.

***Level 1: Sparkplug Compliant MQTT Server***

A Sparkplug Compliant MQTT server MUST support the following:

- QoS 0 (at most once) for data
- QoS 1 (at least once) for state management
- Retained Messages support
- Last Will and Testament (LWT) for state management
- Wildcard available

***Level 2: Sparkplug Aware MQTT Server***

In addition to the requirements of a Sparkplug Compliant MQTT Server, a Sparkplug Aware MQTT Server must have the following additional capabilities:

- Store NBIRTH and DBIRTH messages as they pass through the MQTT Server.
- Make NBIRTH messages available on a topic in the following format: `$sparkplug/certificates/{namespace}/{group_id}/NBIRTH/{edge_node_id}` For example, if `group_id=GROUP1` and `edge_node_id=EON1`, NBIRTH messages must be available on the topic: `$sparkplug/certificates/spBv1.0/GROUP1/NBIRTH/EON1`
- Make NBIRTH messages available on the topic: $sparkplug/certificates/{namespace}/{group_id}/NBIRTH/{edge_node_id} with the MQTT retain flag set to true.
- Make DBIRTH messages available on a topic in the following format: `$sparkplug/certificates/{namespace}/{group_id}/DBIRTH/{edge_node_id}/{device_id}` For example, if `group_id=GROUP1`, `edge_node_id=EON1`, and `device_id=DEVICE1`, DBIRTH messages must be available on the topic: `$sparkplug/certificates/spBv1.0/GROUP1/DBIRTH/EON1/DEVICE1`
- Make DBIRTH messages available on the topic: `$sparkplug/certificates/{namespace}/{group_id}/DBIRTH/{edge_node_id}/{device_id}` with the MQTT retain flag set to true.
- Replace the timestamp of NDEATH messages. If the MQTT server replaces the timestamp, it must set it to the UTC time at which it attempts to deliver the NDEATH to subscribed clients.

The Sparkplug Aware MQTT server extends the state management approach of Sparkplug. In essence, the birth and death certificates are now stored as retained messages and can be accessed using the newly introduced topic structure `$sparkplug/certificates/#`.

The ability to update the timestamp of the NDEATH message is a notable feature in this version. Due to the Last Will feature, these timestamps are stored in the broker. The Last Will message is included in the [MQTT connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection) attempt and contains an invalid timestamp since the actual time of an unconditional client disconnection is unknown. Updating this timestamp through the publication of the LWT message addresses this issue.

## **Benefits of Sparkplug 3.0 for IIoT Applications**

### Enhanced Interoperability

With a more formalized and clarified specification, Sparkplug 3.0 promotes better interoperability among IIoT devices, systems, and platforms. This enables seamless integration and communication within industrial environments.

### Efficient Data Synchronization

The extended state management capabilities of MQTT Sparkplug 3.0 ensure efficient and synchronized data updates across connected devices. This feature becomes especially valuable when dealing with large-scale IIoT deployments.

### Streamlined Deployment

The subset requirements for MQTT servers ensure that existing MQTT v3.1.1 servers can be leveraged, reducing the need for extensive infrastructure changes during the adoption of Sparkplug 3.0.

## **Sparkplug Compatibility Program**

The Sparkplug Compatibility Program enables software and hardware vendors to prove compatibility with Eclipse Sparkplug and MQTT-based IoT infrastructure. This program facilitates seamless integration with common devices and networks in industrial IoT, ensuring certified solutions and easy procurement.

Certified vendors provide confidence in product adherence to Sparkplug specifications, enabling smooth interoperability and streamlined implementation. Vendors undergo open-source tests to confirm compliance with the Sparkplug Technical Compatibility Kit (TCK). Successful products are added to the official list of compatible products, visible on the [Sparkplug Working Group's website](https://www.eclipse.org/org/workinggroups/eclipse_sparkplug_charter.php). The Sparkplug Compatible logo showcases compatibility.

Customers can trust that certified products have undergone rigorous testing and meet the required standards.

The program offers benefits to both vendors and customers:

- Fostering Seamless Integration

  The program promotes interoperability, simplifying integration for system integrators and end-users. Certified components work seamlessly together, allowing organizations to build robust IoT solutions with confidence.

- Encouraging Innovation and Collaboration

  Certification drives innovation and collaboration. Vendors align their products with Sparkplug, fostering feature-rich, interoperable solutions. Knowledge sharing and collaboration among vendors create a vibrant ecosystem.

## **Conclusion**

Sparkplug 3.0 brings significant advancements and formalization to the MQTT Sparkplug protocol for IIoT applications. With improved clarity, explicit specifications, and alignment with MQTT 5.0, Sparkplug 3.0 offers enhanced interoperability, efficient data synchronization, and streamlined deployment in industrial environments. As the IIoT ecosystem continues to evolve, Sparkplug 3.0 provides a robust and standardized solution for reliable and scalable communication within IIoT networks. 

As the world’s leading [open-source MQTT broker, EMQX](https://www.emqx.io/) is the main component of infrastructure to manage all Sparkplug 3.0 message traffic. [Neuron, an IIoT connectivity server](https://neugates.io/), can act as an edge node and assist OT devices to be smarter and to report Sparkplug 3.0 messages in an asynchronous way.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
