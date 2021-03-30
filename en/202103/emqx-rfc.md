
To make our open source projects moving forward in a more innovative, positive, and efficient rapid iterative state, the EMQ X team announced that started to officially adopt the RFC process to collect suggestions from the community and to continuously improve the product's functions.

> RFC (Request For Comment) is a kind of process to ensure that major feature updates and architectural changes move forward smoothly. 



We have named the GitHub repositories that manage RFC as EIP, in full: EMQ X Improvement Proposals.

Project address: [https://github.com/emqx/eip](https://github.com/emqx/eip)

 

## Why EMQ X EIP is needed

[EMQ X](https://github.com/emqx/emqx) open source projects have developed to become more powerful, and its project architecture becomes more complex. The design and implementation of some new features may affect the system architecture and existing features to a greater or lesser extent. Therefore, the team needs to carefully discuss and evaluate the new features before planning and implementing them. At the same time, as the user and community groups have grown, we have received more and more suggestions from users for great and innovative features for EMQ X, and the desire to incorporate these ideas into future versions of EMQ X.

This is why the EIP project was created. We will provide a platform for you to record the detailed information of your ideas and designs or implementations of new features. When some ideas or updates involve changes to the system architecture, features, APIs, etc. - as mentioned above - that require a discussion and review process before development can begin, the EIP is a more appropriate way to ensure that the EMQ X team and the community reach a consensus.

EIP has the following three characteristics:

- Open Innovation Collaboration. EMQ X is an open source project and we follow the principles of open source projects - not only will we keep the source code open, but we will also open up the design and discussion of features to bring EMQ X closer to the community. Everyone can participate and everyone can learn about it. By having more participants to help, guide and improve the design of EMQ X, more creative ideas can be successfully implemented.
- Ensuring Project Stability. The EIP allows us to try our best to minimize the impact of each iteration on existing users. The ideas, suggestions, and designs incorporated will be carefully reviewed and discussed to ensure that every feature input is reliable and stable to the greatest extent possible, providing the best possible experience for everyone.
- Tracking Designs. Through the EIP, each feature idea and design will contain a PR and a record of the discussion. When we add, remove or modify a feature, we want users can see that the thoughts and compromises we have made on it through each EIP document and the PR behind it. This is important for the long-term development of EMQ X and for developers who want to learn more about EMQ X.

Besides that, a small number of feature updates, bug fixes, and code changes can still be implemented by following the normal GitHub process of submitting issues, launching Pull Requests and Code Reviews.

![EIP.png](https://static.emqx.net/images/8599d98ae5ebaaa4ce1c87e7ea2700ea.png)


## How to use EMQ X EIP

All the EIP are in form of Markdown(*.md) files.

Each new EIP will be created by submitting a Pull Request and is discussed and approved before being moved to the `active` directory. Once this has been designed and completed, it will be placed in the `implemented` directory.

Before submitting your EIP, please read 0000-proposal-template, which is a template for demonstrating the EIP format and is roughly structured as follows:

```markdown
# An Example of EMQ X Improvement Proposal

## Change log

* 2020-10-21: @emqxplus Initial draft
* 2020-02-05: @terry-xiaoyu Restructure
* 2021-02-21: @zmstone Add 'Declined Alternatives' section

Used to record changes, including the date, author, and content of the change.

## Abstract

A short (~200 word) description of the technical issue being addressed.

## Motivation

This section should clearly explain why the functionality proposed by this EIP is necessary. EIP submissions without sufficient motivation may be rejected outright.

## Design

This section should describe the design of the feature in detail. If it is a change to the architecture, some diagrams may be necessary.

## Configuration Changes

This section should list all the changes to the configuration files (if any).

## Backwards Compatibility

This sections should shows how to make the feature is backwards compatible. If it can not be compatible with the previous emqx versions, explain how do you propose to deal with the incompatibilities.

## Document Changes

If there is any document change, give a brief description of it here.

## Testing Suggestions

The final implementation must include unit test or common test code. If some more tests such as integration test or benchmarking test that need to be done manually, list them here.

## Declined Alternatives

Here goes which alternatives were discussed but considered worse than the current. It's to help people understand how we reached the current state and also to prevent going through the discussion again when an old alternative is brought up again in the future.
```



You can also refer to the EIP documents in the implemented instances. Through referring to the implemented instances to edit the document for your ideas and suggestions.



## Start your first EMQ X EIP

So far, we would like to welcome all readers, users, and developers to actively participate in the EIP project and to suggest new and powerful features and ideas for EMQ X. 

We use the EMQ X EIP to make every voice heard and echoed, and allow EMQ X to become the open source project which all community users will be proud of. A great open source project for the IoT era will be created by us all.

