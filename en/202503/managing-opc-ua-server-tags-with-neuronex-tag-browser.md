## Introduction

[**OPC UA (OPC Unified Architecture)**](https://www.emqx.com/en/blog/opc-ua-protocol) is a cross-platform, service-oriented communication protocol widely used in industrial automation and the Industrial Internet of Things (IIoT). It provides a standardized framework for interoperability between industrial devices and systems. As a core technology in industrial communication, OPC UA offers high security, flexibility, and scalability, making it particularly suitable for Industry 4.0 and IIoT applications. It is gradually becoming the universal standard for industrial device interoperability.

This article will introduce how NeuronEX's tag browser feature can help users manage OPC UA device tags more efficiently.

## Preparation

Before using the tag discovery feature, we need to connect an OPC UA device.

1. Log in to the NeuronEX console and navigate to the "Data Collection" -> "South Devices" page.
2. Click the "Add Device" button to go to the device addition page.
3. Select the "OPC UA" plugin and enter the OPC UA server endpoint URL.
4. Fill in the device name, for example, `opcua1`, and click the "Add Device" button.

![image.png](https://assets.emqx.com/images/1e57e3a333961d54487609e9b63f3165.png)

Once the device is added, return to the South Devices page. You will see the newly added `opcua1` device and its connection status should be "Connected."

![image.png](https://assets.emqx.com/images/96178c4593c7ee6416e0fd75452e20ac.png)

## Tag Browser Feature

With the preparation complete, let's dive into the main topic: using the tag browser feature to efficiently manage OPC UA server tags.

### Tag Browser

1. Click the "Device Configuration" button in the operation column corresponding to the `opcua1` device.

   ![image.png](https://assets.emqx.com/images/ecccd2b9dde77db5261e3377684753a8.png)

1. On the device configuration page, switch to the "Tag Browser" tab on the far right.

2. In the "Tag Browser" tab, click the "Scan" button. NeuronEX will automatically scan the OPC UA server's address space for tag information.

   ![image.png](https://assets.emqx.com/images/14657d06e9b5f5150308cfa8988501b9.png)

1. After the scan is complete, you will see the top three nodes listed in the node information.

   ![image.png](https://assets.emqx.com/images/c56017cfe7c4a8a4e443a779f710bc67.png)

1. Click the triangle icon in front of a node to expand and display all its child nodes. If a child node is a tag, the data type column will show the corresponding data type information.

   ![image.png](https://assets.emqx.com/images/65f2f8bef4ea86ae240f1a1932b0dec0.png)

### Add Tags to a Collection Group

If you want to add certain tags to the device's collection group, follow these steps:

1. Select the tags you want to add and click the "Add Tags to Group" button. You can also select the `Simulation` node to select all its child nodes.

   ![image.png](https://assets.emqx.com/images/c590165f4d7f90eced2e5050e0d54814.png)

1. In the "Select or Create a Group to Add Tags" dialog, if you want to add the tags to an existing group, simply select the group from the dropdown menu. For this example, we will create a new collection group.

2. Configure the group name (e.g., `group1`) and the collection interval, then click the "Create Group and Add Tags" button. You will be redirected to the tag addition page.

   ![image.png](https://assets.emqx.com/images/74160c64fd164a5661010b9716da82d3.png)

1. On the Add Tag page, you will see the six selected tags with their data types. You can further modify the tag names, read/write types, and other configurations. Once done, click the "Create" button to complete the tag addition.

   ![image.png](https://assets.emqx.com/images/f4a0cfba1f9c8a180f86027b85a0416e.png)

After the tags are created, you can view real-time data collection results on the data monitoring page.

![image.png](https://assets.emqx.com/images/11bc44bb4252a5336ad35655a4ee5a64.png)

### Export Tag

To export selected tags as a tag table:

1. Return to the "Tag Browser" tab.

2. Select the tags you want to export and click the "Export Tags" button.

   ![image.png](https://assets.emqx.com/images/b47fa838db89473e95612a49f09570fe.png)

1. An Excel file will be downloaded to your local machine. The file will contain the relevant information of the six selected tags. After exporting the tag table, you can locally edit and save the tag information. This allows for further customization and organization of the tags according to your specific requirements. Once the edits are complete, you can import the updated tag table back into NeuronEX for use.

![image.png](https://assets.emqx.com/images/841c2df6b7b1c8e464ebf209b8bc837b.png)

## Conclusion

We have now fully introduced NeuronEX's tag browser feature. With this feature, users can efficiently manage OPC UA server tags, enabling rapid integration of OPC UA devices.

Download NeuronEX now and start your industrial digital transformation journey: [Try EMQX Cloud or EMQX Enterprise for Free | Download EMQX](https://www.emqx.com/en/try?tab=self-managed) 

For more NeuronEX features, please refer to the documentation: [Product Overview | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
