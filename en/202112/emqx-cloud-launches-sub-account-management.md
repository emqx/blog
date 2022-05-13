[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed cloud-native MQTT message service for the IoT field launched by EMQ, which can connect massive IoT devices through reliable and real-time IoT data movement, processing and integration, accelerate the development of enterprise IoT applications and eliminate the burden of infrastructure management and maintenance.

For enterprise application software, permission design is an important module. The diverse organizational structures of each enterprise will produce different business processes. Therefore, the application software needs to have a complete permission management function, enabling different users to see different modules, operate different functions and see different ranges of data after logging in to the system. Otherwise, problems such as data leakage and authority confusion are extremely likely to occur during the use process, which will affect the enterprise's management process and cause unpredictable losses.

In the last update, we launched the [Multi-Project Deployment Management function](https://www.emqx.com/en/blog/emqx-cloud-realizes-multi-project-deployment-management). Through this function, the deployment of different projects is managed separately, which is the first step to realizing comprehensive permission management.

Recently, the **Sub-account management function is also officially launched**. This function can support different roles in the enterprise to carry out the operation and management with the corresponding permission of the account, making the business process of the enterprise clearer and easier to manage.

## Application scenarios for sub-account management

![Application scenarios for sub-account management](https://assets.emqx.com/images/06c3c78db866209a77f81b46235c7533.png)


### Classified management of production and development test environments, without mutual interference

For most enterprise customers, a SaaS service needs to be tested before it is officially applied to the actual business. In this regard, EMQX Cloud has opened a free trial of the basic version for 30 days and the professional version for 14 days, which allows users to investigate and understand products in the early stage, and saves the cost in the test and development stage.

After the deployment is officially put into production, enterprise business changes will inevitably bring some changes. At this time, if you rashly modify the deployment in operation, it is likely to cause unnecessary losses. Then, the multi-project management and sub-account management of EMQX Cloud can be used.

By **distinguishing the deployment of the development test environment from the production environment,** and allocating them to the 「production environment」 and 「test environment」 for management, we can prevent modification errors. At the same time, the administrator can **give different project permissions to internal development testers and business personnel to avoid unauthorized operations.**

### Self-service query for financial audit is provided to improve work efficiency greatly.

Financial management is an indispensable part of the enterprise business. For financial reimbursement or reconciliation in the past, the financial personnel needed to inform the technical staff of the required bill and invoice information. Then the technical staff logged in to the financial module to download the required financial documents. In this link, errors may occur due to poor information communication, resulting in unnecessary repetitive operations and low efficiency.

Through sub-account management, you can invite enterprise financial personnel to become the financial specialist user of the account. After logging in to the console, the financial specialist user can view (read-only and non-editable) the deployment of all projects and perform account checking and account reconciliation to deploy different projects. In the whole process, there is no need to worry about the impact of deployment status/settings caused by financial misoperation. **The efficiency of the independent financial queries is improved, and there is no need to trouble technical staff to help check accounts.**

## How to use the sub-account management function

### Set the role of the sub-account

First, we will explain the several account roles currently supported by EMQX Cloud. At the same time, it needs to be explained that a role can be assigned to multiple accounts, which can also have multiple roles. The relationship between roles and accounts is many-to-many.

- **Administrator**: The administrator has all the access to the platform and is the super administrator in the subaccount system.
- **Project Administrator**: Project Administrators have permission to view and modify projects and to modify and delete deployments.
- **Project User**: Project users have permission to view the project, and the permission to view and edit the deployment.
- **Accountant**: Accountants have financial management permissions and can view projects and deployments. They can manage the billing, balance, invoices, etc.
- **Auditor**: Auditors can view projects, deployments, sub-users, and Accountants. The audit role addresses the need for internal company audits and can have viewing permissions to various platform features.

After registering on the website ([https://www.emqx.com/en](https://www.emqx.com/en)), you will become the administrator user of the account by default. You can enter the console, find 「User Management」 in the menu bar at the upper right corner, click 「New User」, enter the email and password of the sub-account you want to authorize, and assign it different roles (multiple roles can be selected).

![New user](https://assets.emqx.com/images/ba00b83715c46d7725c40c4ad7c03aa7.png)
 

After that, the sub-account user will receive the corresponding login link in the mailbox. After entering the mailbox and password, he can log in and perform the corresponding operation.

![mailbox](https://assets.emqx.com/images/36b4e90118c6ca83ee47ba8d3a8eb6b1.png)

> Note: 1 for account verification and first login, 2 for subsequent sub-account login.

### **Associate the sub-account with the project**

You can find the 「Project Center」 in the menu at the upper right corner, where you can find all the projects you have created. By default, the projects are open to all sub-accounts, but the operational permissions change with the change of roles.

> Note: The projects you create independently support association with sub-accounts.

Click on the upper right corner of the specified project

![project](https://assets.emqx.com/images/560713ac83e8551df400263a30049ce8.png)

Click「Add」, enter account keywords, and related accounts will be automatically associated. Roles that can be granted include "Project Administrator" and "Project User".

![roles](https://assets.emqx.com/images/92243347a6ad10eff2fc9796835e902e.png)

The EMQX Cloud team is committed to providing users with easy, convenient, automated and [fully managed MQTT cloud services](https://www.emqx.com/en/cloud). We will continue to improve the functional development of the permission management module to bring users a more pleasant product experience.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
