We are excited to announce that [EMQX Enterprise](https://www.emqx.com/en/products/emqx) 5.3.0 is now available!

The latest release introduces multiple enterprise features, such as audit logs, Dashboard Role-Based Access Control(RBAC), and one-stop login based on single sign-on (SSO). These enhancements elevate the security, manageability, and governance of your enterprise deployments. Moreover, this new version brings several improvements and bug fixes, contributing to an overall boost in performance and stability.

## Audit Logs

Audit Logs is a feature designed to capture critical operational activities within a software or system. EMQX‘s support for audit logs enables you to monitor significant actions in real-time during cluster management and configuration, facilitating compliance adherence for organizations.

This new feature can record all change-related operations originating from the [Dashboard](https://docs.emqx.com/en/enterprise/v5.3/dashboard/introduction.html), [REST API](https://docs.emqx.com/en/enterprise/v5.3/admin/api.html), and [Command Line](https://docs.emqx.com/en/enterprise/v5.3/admin/cli.html), such as user logins and modifications to resources (including clients, access controls, and data integrations). The audit logs capture details such as the target of each operation, the initiating user, source IP address, browser characteristics, key parameters, and the outcome of the action. This information is readily accessible and searchable by enterprise users, ensuring efficient compliance and security audits during ongoing operations.

In this EMQX version, audit logs are exclusively written to log files. Future iterations will offer easy-to-use search and viewing functionality on the Dashboard, streamlining the audit management process.

## Dashboard RBAC

The EMQX Dashboard plays a pivotal role in the management and configuration of EMQX clusters. In large enterprises, team members often have varying degrees of responsibility, necessitating the allocation of Dashboard access according to their roles—a security best practice.

This release introduces Role-Based Access Control (RBAC) for permission management. RBAC assigns distinct access privileges to users based on their roles within the organization. This feature streamlines permission management, enhances security through access control, and improves organizational compliance, making it an essential security management mechanism within the Dashboard.

Presently, the Dashboard is preconfigured with two distinct roles:

**Administrator**

The Administrator role pocesses complete administrative authority over all EMQX features and resources, including client management, system configuration, API key management, and user administration.

**Viewer**

Viewers possess read-only privileges, granting them access to EMQX data and configuration details. They can view client lists, access cluster metrics and status reports, and inspect data integration configurations. However, they lack authorization for creating, modifying, or deleting operations.

In forthcoming releases, there will be an expansion in RBAC privilege management through the REST API, accompanied by the addition of more predefined roles. These developments aim to cater to users' requirements for finer-grained access control and enable EMQX to better adapt to the intricate management demands of large-scale enterprise users.

## SSO for Simplified Dashboard Login

Single Sign-On (SSO) is an authentication method that enables users to access multiple applications or systems using a single set of credentials (e.g., username and password) without the need for separate authentication for each application.

The EMQX Dashboard introduces SSO functionality based on LDAP and SAML 2.0 in this release. With SSO activated, users can effortlessly log in to the Dashboard using their existing Enterprise Management System (EMS) accounts. This significantly reduces the need to remember multiple passwords, thus minimizing the risk of password exposure and potential hacking incidents. Enterprises can centrally manage user identities and permissions, simplifying the process of handling, configuring, and deactivating user accounts.

At present, the EMQX Dashboard supports integration with LDAP SSO services, including those offered by [OpenLDAP](https://www.openldap.org/), [Microsoft Entra ID](https://azure.microsoft.com/en-in/products/active-directory) (formerly Azure Active Directory), and SAML 2.0 SSO services from identity providers like [Okta](https://www.okta.com/), [OneLogin](https://www.onelogin.com/), among others.

## Additional Updates

- We’ve introduced cluster optimization configuration options that can be finely tuned to meet your deployment requirements. This adjustment can significantly reduce the startup time of the replica nodes.
- We've added a new SQL rule function called `bytesize`, which allows you to determine the size of byte strings effectively.

## Bug Fixes

We've also resolved several important bugs:

- Fixed the issue that caused logging to stop when the handler rotation size was set to `infinity` in file logger. [#11682](https://github.com/emqx/emqx/pull/11682)
- Fixed the issue where log lines were not valid JSON but were prefixed with timestamp and level info when the log format `log.{handler}.formatter` was set to `json`. [#11661](https://github.com/emqx/emqx/pull/11661)

For a comprehensive list of feature changes and bug fixes, please refer to the [EMQX Enterprise 5.3.0 changelog](https://www.emqx.com/en/changelogs/enterprise/5.3.0).



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
