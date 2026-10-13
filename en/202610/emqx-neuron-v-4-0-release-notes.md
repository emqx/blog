[EMQX Neuron](https://www.emqx.com/en/products/emqx-neuron) 4.0 is now officially available.

Rather than simply adding features, Neuron 4.0 removes the built-in database, data exploration module, Node-RED, and AI assistant. These features are not inherently problematic, but they overlap with tools many plants already use.

A modern industrial connectivity server should focus on connecting machines, processing data at the edge, and delivering it to systems designed for storage. It does not need its own historian.

With this focus, EMQX Neuron 4.0 adds drivers for Brother and Mazak CNC machines, improves the Beckhoff ADS, Siemens, and EtherNet/IP drivers, and simplifies tag list creation.

## What Came Out, And Why



| Removed                                                      | Why                                                          |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Data exploration**, including the built-in Datalayers database, the query-based analysis on top of it, and the DataStorage application that wrote to it | Every plant that wants history already runs a historian or a time-series database. The rules engine writes to InfluxDB, SQL databases and Redis, so the data goes where the customer already keeps it. |
| **Built-in Node-RED**                                        | The rules engine can do the same in SQL, which is easy to review in pull requests, diff between versions, and maintain. A visual canvas offers none of these advantages. |
| **LLM features**, including the AI assistant and AI Q&A      | Model inference remains unchanged. Only the LLM features were removed, as they belong in the cloud, not in a factory cabinet. |
| **Syslog forwarding**                                        | Metrics go to Prometheus Pushgateway and alerts to a webhook, covering Syslog's role in a format existing monitoring tools can use. |

The Docker images are now leaner, with unnecessary system dependencies removed. The standard image is about a quarter of its former size, reducing patching, security reviews, and the learning curve for new engineers.

## What EMQX Neuron 4.0 Adds



### Two CNC drivers



- **Brother CNC** connects to Brother machining centres over Ethernet or serial, using the Brother NC protocol. It collects axis coordinates, spindle and tool data, alarms, part counts, program numbers, PLC devices and tool offsets.
- **Mazak CNC** listens for the status packets a Mazak CNC sends over UDP, and turns each field into a tag. It sends no requests to the machine.

Both drivers are read-only and join existing drivers for FANUC, Siemens, Mitsubishi, HEIDENHAIN, and other CNC controllers. They require a trial or commercial license; the free license does not cover CNC drivers.

### Better drivers



- The **Beckhoff ADS** driver imports tags from TPY files made in both TwinCAT 2 and TwinCAT 3.
- The **Siemens** driver supports array data types.
- The **EtherNet/IP** driver is compatible with more devices. It can read and write tags on more kinds of equipment.

### Tag lists that are quicker to build



- **CSV import and export.** Tags can be imported from a CSV file and exported to one. A tag list becomes a file you can edit in a spreadsheet, copy between instances and keep under version control.
- **Search in the OPC UA browser.** When you browse an OPC UA server's address space, you can now search and filter the tags. On a large server, that is the difference between finding a node and scrolling for it.

## What Did Not Change



This matters as much as the lists above, because it is the part you rely on.

- **Every driver from 3.x is still there.** More than 70 industrial protocols across PLC families, CNC controllers, power and energy standards and building systems, on Ethernet and on serial.
- **The collection model is the same.** Tags belong to collection groups. Each group is polled at its own interval, and every application that subscribes to the group gets the same data. Adding a destination does not add a read at the device.
- **The rules engine is the same.** Streaming SQL with more than 160 functions and five window types. Model inference with ONNX models stays.

## Two Container Images, Both Much Smaller



| Image                            | What it carries                                              | Download size | When you need it                             |
| :------------------------------- | :----------------------------------------------------------- | :------------ | :------------------------------------------- |
| `emqx/neuronex:<version>`        | The standard image, with the Python runtime and the rules engine's Python SDK | Under 110 MB  | The default, and the one Python plugins need |
| `emqx/neuronex:<version>-extend` | The standard image plus FFmpeg and ONNX                      | Under 275 MB  | Model inference and video sources            |

In v3.9, the standard image was about 450 MB. The `-ai` image, which carried model inference, was over 700 MB. A smaller image pulls faster over a slow plant network and leaves more room on a small gateway.

The `-ai` image is gone, and model inference now needs `-extend`. **If you run models today, change your image tag before you upgrade.**

## Third-Party Sign-in, Not Single Sign-on



The console supports sign-in through any OAuth 2.0 provider. In v4.0, this is called third-party sign-in: it verifies authentication but does not read user identities or map roles. Anyone authenticated by the provider can sign in as an administrator.

This is not single sign-on (SSO). **Restrict access at your identity provider, not in Neuron.**

## Before You Upgrade



A short checklist, in the order that matters.

1. **Check whether you use anything that was removed.** Data exploration, the built-in database, the DataStorage application, Node-RED, the AI assistant or syslog forwarding. If you do, plan where that job goes before you move.
2. **Change your image tag if you run models.** `-extend` carries the inference runtime.
3. **Mount** `plugins/` **as well as** `data/`**.**
4. **Back up both**, plus anything you have edited under `etc/`.

## Where to Start



If you are new to EMQX Neuron, the fastest way to see it is to install it and point it at something.

The permanent free licence covers 30 data tags with no time limit, so you do not need to request anything before you begin. A trial licence lifts that to 1,000 tags for 15 days and unlocks every driver, every application and the full processing engine. A trial licence binds to a hardware ID, and a container does not have one. If you run in a container, ask EMQ for an unbound licence.

Install it in one line:

```shell
curl -fsSL emqx.sh/neuron | bash
```

The script picks a .deb, .rpm, tar.gz or Docker install for you. EMQX Neuron runs on Linux, on 64-bit x86 and on both 32-bit and 64-bit ARM, so the same product runs on a gateway and on a server.

If you are moving from KEPServerEX or Litmus Edge, EMQ's [online migration tool](https://www.emqx.com/en/products/emqx-neuron/migrator) converts their driver and tag configurations into files EMQX Neuron can import. Run the two side by side, compare, then switch.

**Experience EMQX Neuron 4.0 today**: [Download EMQX Neuron](https://www.emqx.com/en/downloads-and-install/neuronex) 

**Learn more about this release**: [www.emqx.com/en/changelogs/neuronex/4.0.0](https://www.emqx.com/en/changelogs/neuronex/4.0.0) 



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
