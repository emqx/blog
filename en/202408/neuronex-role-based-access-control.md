As organizations advance their digital transformation, securing data and information becomes ever more crucial. Traditional access control methods, which often require configuring permissions for each user individually, are not only complex but also prone to vulnerabilities, making it challenging to keep pace with evolving business needs. Role-based access control (RBAC) streamlines privilege management by defining specific roles and their associated permissions. This approach not only ensures effective control over users' access to sensitive information and systems but also reduces the operational and maintenance workload for enterprises.

NeuronEX, an industrial edge gateway software, supports a wide range of industrial protocols and offers robust edge computing capabilities. It enables data collection from industrial equipment, integration of industrial system data, edge data filtering and analysis, AI algorithm integration, data forwarding, and platform connectivity. These features provide low-latency data access management and intelligent analysis services tailored to industrial scenarios.

In this blog, we will explore the role-based access control feature in NeuronEX. This function allows users to create various roles, each with distinct operational privileges, thereby achieving privilege isolation and enhancing the security, compliance, and flexibility of user data.

## User Management

The system includes a built-in super administrator user named `admin` whose password can be changed after the initial login. To enable role-based access control, NeuronEX introduces a new user management feature, accessible via the **Users** button on the sidebar.

![NeuronEX Dashboard](https://assets.emqx.com/images/901e3b59b9638fde64ae9497ef9d116a.png)

To create a new user, click the **Create User** button. On the pop-up page, you will need to enter the new user's name, password, role, and remark. The Role drop-down box allows you to select between the Administrator and Viewer roles. Once all the user information is filled out, click the **Submit** button to save the new user.

![NeuronEX Dashboard: Create User](https://assets.emqx.com/images/52a1b0645c76051950653994f99820c0.png)

Additionally, after a user is created, you can edit the user's information, change password, or delete the user from the user list.

## Access Control

NeuronEX's permissions are closely tied to predefined roles, and it does not support custom role permissions. The role permissions are determined by NeuronEX, with the Administrator role granting full control over NeuronEX, including the ability to view, create, modify, and delete all configurations. In contrast, the Viewer role is limited to viewing configurations only.

Once a user is created, they can log into the system using their credentials. Since the user is assigned either the Administrator or Viewer role at creation, their permissions are automatically established upon login. Users assigned the Viewer role will find that some editing buttons in the frontend are disabled.

![Southbound devices](https://assets.emqx.com/images/e0274d4d15ea6dcf69fc747afa530983.png)

<center>The Administrator role can create new southbound devices.</center>

<br>

 ![Add device button](https://assets.emqx.com/images/c1130fb8ece483f58b131b0cf70fe338.png)

<center>The Viewer role cannot create new southbound devices.</center>

<br>

In addition to frontend access control, the access control mechanism also applies to NeuronEX API requests. Users must first call the /api/login interface to obtain a Token, which is then used to access the corresponding NeuronEX API. A Token obtained with the Administrator role can request any API, whereas a Token obtained with the Viewer role will return a 403 status code when attempting to access APIs beyond its permissions.

## Conclusion

This blog describes the role-based access control features in NeuronEX. By allowing the creation of multiple users and assigning them either the Administrator or Viewer role, with corresponding control permissions, NeuronEX provides a robust access control system. This ensures that when a user makes a request, their access is appropriately restricted based on their role. This feature has been supported since version 3.3.0, and you are welcome to explore it.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
