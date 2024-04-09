## Introduction

Event History, also known as Lifecycle Events, is a crucial record system that tracks significant occurrences or events within the IoT system. These events encompass a wide range of data, including online/offline events, device statuses, message delivery events, etc.

EMQX Dedicated v5 will soon introduce Event History as a new feature, offering an out-of-the-box method to observe and analyze device behavior over time. Users will gain in-depth data insights for their MQTT connections and manage them better through this advanced feature.

## Why Event History?

### Effective Diagnosis 

Event History allows users to review event details, enabling them to diagnose issues promptly and efficiently. By identifying patterns or anomalies in system behavior, users can troubleshoot problems effectively and implement appropriate solutions.

### **Regulatory Compliance**

In many industries, regulatory requirements mandate the maintenance of detailed records of system activities. Event History ensures compliance with these regulations by providing a comprehensive audit trail of all relevant events, facilitating regulatory reporting and compliance efforts.

### **Insights into System Behavior**

Event History provides valuable insights into the behavior of the IoT system over time. By studying trends and patterns in event data, users can gain a deeper understanding of how the system operates under various conditions, helping them make informed decisions and optimize system performance.

## What Kinds of Events are Recorded in Event History?

EMQX Dedicated’s Event History feature contains the following events, which are continually updated.

- **Client Connected**: the event of the client connected to the broker
- **Client Disconnect**: the event of the client disconnected
- **Client Subscribe**: the event of the client subscribing to a topic
- **Client Unsubscribe**: the event of the client unsubscribing to a topic
- **Session Create**: the event of the session was created
- **Session Terminated**: the event of the session expiry when “clean session” is false
- **Message Dropped**: the event of the message has been dropped due to the message queue being full or expiry.

Users can quickly pinpoint the potential causes and effectively troubleshoot issues by examining details such as “client_id“, “topic, “result“, etc. This ensures smoother system operations overall.

## Be the First to Experience Event History

We're currently in the testing phase and inviting interested customers to join our exclusive private beta test. Enter your email on the [Event History Private Beta](https://www.emqx.com/en/cloud/event-history-private-beta) Page and secure your spot on the waitlist. We'll keep you updated and notify you as soon as it's ready for you to explore. Don't miss this opportunity to be at the forefront of innovation!

![Event History Private Beta Page](https://assets.emqx.com/images/0bd19aac1ad51c8a3eb513bbf6d5a4f6.png)

***Please be aware that your email address must be a valid EMQX Platform account, and only EMQX Dedicated v5 deployments in the AWS Virginia region can enable Event History.**
