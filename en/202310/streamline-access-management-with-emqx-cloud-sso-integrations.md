[EMQX Cloud](https://www.emqx.com/en/cloud) is dedicated to providing a fully managed MQTT service that delivers excellent connectivity and integration solutions for IoT businesses. The latest addition to its features is Single Sign-on (SSO), which enables users to access all trusted applications with just one single sign-on. With this feature, users can now log in to EMQX Cloud with their identity provider accounts, eliminating the need for repetitive password input work and improving account security.

## What is SSO?

SSO, standing for Single Sign-On, allows users to log in to multiple related applications and services using a single set of login credentials, such as a username and password. Once logged in, users can access these services securely without having to log in again during the session.

### How SSO Works

SSO is based on a digital trust relationship between a group of related, trusted applications, websites, and services(service providers*)* and an SSO solution(identity provider). 

In general, SSO authentication works as follows:

1. A user logs into one of the trusted applications or an SSO solution with all trusted credentials.
2. When the user is successfully authenticated, the SSO solution generates a session authentication token containing specific information about the user's identity - a username, email address, etc. This token is stored with the user's web browser or on the SSO solution server.
3. When the user attempts to access another of the trusted applications, the application checks with the SSO server to determine if the user is already authenticated for the session. If so, the SSO solution validates the user by signing the authentication token with a digital certificate, and the user is granted access to the application. If not, the user is prompted to reenter login credentials.

### Benefits of SSO

SSO solutions reduce the number of credentials users need to remember, improve security, and simplify administration and maintenance processes.

Take corporate users as an example: users only need to log in to their company intranet or extranet once. After that, they can access all the applications they need throughout the day without having to log in multiple times. Additionally, SSO improves the security of the organization by significantly reducing the number of passwords users need to remember and the number of user accounts administrators need to manage.

Organizations can benefit from SSO in the following aspects:

- **Avoid password fatigue with one strong password.** Users with lots of passwords to manage often lapse into using the same short, weak passwords - or slight variations thereof - for every application. A hacker who cracks one of these passwords can easily gain access to multiple applications. SSO can reduce scores of short, weak passwords to a single long, complex, strong password that's easier for users to remember - and much more difficult for hackers to break.
- **Help prevent unsafe password storage habits.** SSO can eliminate the need for insecure password management methods like using a password manager, storing passwords in spreadsheets or writing them down on sticky notes - all of which would make passwords easier for the wrong people to steal or stumble upon.
- **Give hackers a smaller target.** According to IBM's Cost of a Data Breach 2021 report, compromised credentials were the most frequent initial attack vector for a data breach, accounting for 20% of all data breaches - and breaches that began with compromised credentials cost their victims $4.31 million on average. Fewer passwords mean fewer potential attack vectors.
- **Simplify management, provisioning, and decommissioning of user accounts.** With SSO, administrators have more centralized control over authentication requirements and access permissions. And when a user leaves the organization, administrators can remove permissions and decommission the user account in fewer steps.
- **Help simplify regulatory compliance.** SSO meets or makes it easier to meet regulatory requirements around protection of personal identity information (PII) and data access control, as well as specific requirements in some regulations - such as HIPAA - around session time-outs. 

### Related Technologies

SSO can be implemented using any of the authentication protocols and services, the more dominant solutions currently are:

**SAML/SAML 2.0**

SAML (Security Assertion Markup Language) is the longest-standing open standard protocol for exchanging encrypted authentication and authorization data between an identity provider and multiple service providers. Because it provides greater control over security than other protocols, SAML is typically used to implement SSO within and between enterprise or government application domains.

**OAuth/OAuth 2.0**

OAuth/OAuth 2.0 (Open Authorization) is an open standard protocol that exchanges *authorization* data between applications without exposing the user's password. OAuth enables using a single log-in to streamline interactions between applications that would typically require separate logins to each. For example, OAuth makes it possible for LinkedIn to search your email contacts for potential new network members.

**OpenID Connect (OIDC)**

Another open standard protocol, OICD uses REST APIs and JSON authentication tokens to enable a website or application to grant users access by authenticating them through another service provider.

Layered on top of OAuth, OICD is used primarily to implement social logins to third-party applications, shopping carts, and more. A lighter-weight implementation, OAuth/OIDC is often to SAML for implementing SSO across SaaS (software as a service) and cloud applications, mobile apps, and Internet of Things (IoT) devices.

**LDAP**

LDAP (lightweight directory access protocol) defines a directory for storing and updating user credentials and a process for authenticating users against the directory. Introduced in 1993, LDAP is still the authentication directory solution of choice for many organizations implementing SSO, because LDAP lets them provide granular control over access the directory.

EMQX Cloud’s SSO feature is implemented via **OIDC**.

## How to Use SSO in EMQX Cloud

First of all, we need to register an account on the EMQX official website and log into EMQX Cloud console. Select "SSO" from the user menu in the upper right corner to enter the SSO configuration page.

![EMQX Cloud console](https://assets.emqx.com/images/d6a2bcb53eb7de704befcfaa147f1798.png)

In this post, we use Microsoft Entra ID (Azure Active Directory) (Azure AD for short) as an example of integration. EMQX Cloud can also interface with other identity providers that support the OIDC protocol.

![Microsoft Entra ID](https://assets.emqx.com/images/9253eb2cdb0f6d38951d333f36538018.png)

Step1. Register application in Microsoft Entra ID (Azure Active Directory).

![Microsoft Entra ID](https://assets.emqx.com/images/d7356c53718f409568efd71092cc14ba.png)

Step2. Config Tenant ID, Client ID and Client Secret in EMQX Cloud - Azure AD SSO.

![Config Tenant ID, Client ID and Client Secret in EMQX Cloud](https://assets.emqx.com/images/b838ce4e94ddaa57429004701db20fe6.png)

Step3. After successful configuration, the SSO login function of EMQX Cloud is enabled. However, you need to assign users in Azure AD and create sub-accounts in EMQX Cloud to complete the sub-account login.

![The SSO login function of EMQX Cloud is enabled](https://assets.emqx.com/images/43ffd899337f95aa50db2d180826fb08.png)

Step4. Assign users or groups to the application in Microsoft Entra ID (Azure Active Directory). 

![Assign users or groups to the application in Microsoft Entra ID](https://assets.emqx.com/images/37339d694e9b934f201c77649ed2e025.png)

Step5. Create a subaccount in EMQX Cloud.

![Create a subaccount in EMQX Cloud.](https://assets.emqx.com/images/1d59a1f61a02137707de9fe8d3e9c8b0.png)

Please check the [documentation](https://docs.emqx.com/en/cloud/latest/feature/sso_overview.html) for detailed configuration instructions and feature descriptions.

## Conclusion

The introduction of SSO in EMQX Cloud marks a significant advancement in user authentication and access management. This addition enables users to effortlessly log in to the EMQX Cloud deployment console like an application with their enterprise account credentials, eliminating the need for separate authentication processes. It offers time and effort savings, improved efficiency and experience, heightened security, and enhanced compliance for large-scale organizations.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
