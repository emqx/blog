For some manufacturers that have been scaled up, the massive amount of user-side device authentication information is generally stored in an internal enterprise database, which not only facilitates management queries, but also increases the security of the data and reduces the risk of data leakage. Although [EMQX Cloud](https://www.emqx.com/en/cloud) supports bulk import of authentication information, in practice, if the number of authentication devices grows rapidly, it often takes a long time to modify or troubleshoot problems.

Previously, EMQX Cloud provided users with the ability to connect to self-built authentication centers through HTTP custom authentication to meet increasingly complex user authentication needs. Besides this, we have recently introduced MySQL and PostgreSQL external auth&acl, which supports direct verification of device authentication information from the user's MySQL or PostgreSQL database, helping to achieve more secure and faster access to a massive amount of devices.

## Feature Introduction

As a fully-managed cloud-native MQTT messaging service, EMQX Cloud allows users to authenticate their devices and control Topic access through the console's Authentication & ACL module. Authentication is performed in the form of username and password, and access control supports three granularities of client ID, username, and all users. Bulk import of CSV files is supported for both authentication and access control.

In addition to storing authentication information in EMQX Cloud, users can also authenticate devices and realize more complex ACL verification logic by verifying user-side authentication information through external authentication authorization.

Users can access the External Auth & ACL feature by accessing the console and going to the left menu bar "Authentication & ACL" -> "External Auth & ACL". For specific configuration and debugging steps, please refer to the interface tips and the auxiliary document at the end of the text.

![EMQX MySQL and PostgreSQL External Auth](https://assets.emqx.com/images/4a8f6181345205dba79aa8eafb76c2e0.png)
 

**MySQL Auth/ACL Example**

![MySQL Auth/ACL Example](https://assets.emqx.com/images/826fb4ad56f45a978cf518872dc5d4f8.png) 


**PostgreSQL Auth/ACL Example**

![PostgreSQL Auth/ACL Example](https://assets.emqx.com/images/1a3c90b57253bf6c2dfd575d884de999.png)


With the External Auth&ACL feature, users can verify authentication information from external MySQL and PostgreSQL databases as the authentication data source, which makes it easier to store large amounts of data quickly and integrate with external device management systems.


>**Notes:**
>
>1. If built-in authentication is also enabled, EMQX Cloud will chain authentication in the order of default authentication first, followed by external authentication
>2. If the current deployment is the standard version, please fill in the public network address for the server address
>3. If the current deployment is professional Plan, you need to create a VPC peering connection, please fill in the intranet address for the server address
>4. If you are prompted with "Init resource failure!", check if the server address is correct, if the security group is enabled, and if the database is allowed to be accessed by the EMQX Cloud cluster



## Operating Instruction

For more details on the use of MySQL and PostgreSQL External Auth & ACL, please refer to:

MySQL Authentication/Access Control: [https://docs.emqx.com/en/cloud/latest/deployments/mysql_auth.html](https://docs.emqx.com/en/cloud/latest/deployments/mysql_auth.html) 

PostgreSQL Authentication/Access Control: [https://docs.emqx.com/en/cloud/latest/deployments/pgsql_auth.html](https://docs.emqx.com/en/cloud/latest/deployments/pgsql_auth.html) 


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
