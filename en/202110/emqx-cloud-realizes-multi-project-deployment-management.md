In the actual business applications of enterprises, permission management is often a major focus. Whether permission management is sufficiently detailed and flexible is not only related to the information security of enterprises, but also closely related to the refinement degree and efficiency of enterprise management.

## EMQX Cloud is upgraded to meet various management needs

As an enterprise-level fully managed MQTT message service, [EMQX Cloud](https://www.emqx.com/en/cloud) provides convenient and easy-to-use operation and maintenance management services for enterprises of different sizes. In the process of serving our customers, we find that there are usually different organizations and projects within the enterprise. The managers and users of a technical facility service may not be in the same organization, and the management needs and purposes are different.

In the recently updated EMQX Cloud, we introduced the concept of 「Project」to solve this problem.

An enterprise user can create multiple Projects and create deployments under these Projects. Through the multi-project deployment management function, the deployment of different projects can be managed separately to meet the management needs of different organizations.

**Achieve multi-project deployment management through a few easy steps**

Project management focuses on project dimensions, and each project can contain one or more deployments. Each account will have a default project. If no other projects are created, the already created deployments and new deployments created will belong to the default project by default.

![EMQX Cloud multi-project deployment management](https://assets.emqx.com/images/1f9dbede32d3a47cdb19c30cc9fddd30.png)


## Create a project

1. After logging in to the console, click 「Projects」 to enter the project management interface.

![EMQX Cloud Projects](https://assets.emqx.com/images/74af1d23eee8d074fcd4872ef3228afe.png)

Project management

![EMQX Cloud Project management](https://assets.emqx.com/images/331790a59df59613fa687f856628daff.png)

2. Click 「New Project」, fill in the project name and description, and click 「Confirm」. Then, you complete the creation of the project.

![EMQX Cloud New Project](https://assets.emqx.com/images/7dbcaa7d4817463cada87e60f01ac7df.png)

You can find the created project in the project list on the left

![EMQX Cloud created project](https://assets.emqx.com/images/60160b915801f8497963d062ac9c7b61.png)

 
## Manage the deployment under the project

### Create a new deployment

Select the project, click 「New Deployment」, and follow the guide to select the specification for configuration. Then, you create a new deployment under the project.

![EMQX Cloud New deployment](https://assets.emqx.com/images/1b941706216ae2533061a28418af165b.png)

### Move existing deployment

Find the deployment that needs to be moved, move the mouse to the upper right corner of the deployment, and click 「Move to」.

![EMQX Cloud Move existing deployment](https://assets.emqx.com/images/180963fe2c9340fa9f8736a795f86dc8.png)

In the drop-down list, a list of current projects will appear. After selecting anyone in the list, you can move the deployment to the specified project.

![EMQX Cloud select projects](https://assets.emqx.com/images/bf2073307dae44effaa9cfcd26eb3a5b.png)

> Note: A deployment can only belong to one project, and multiple deployments can be managed under one project.


### View all deployments

Click「All Deployments」on the right side of the project list, and you can view all deployments in the current account.

![EMQX Cloud View all deployments](https://assets.emqx.com/images/86ce6edb2e5ddd1ee68998884fcc462e.png)

Overview of all deployments under your account

![Overview of all deployments](https://assets.emqx.com/images/2f5f431fe041d261e09068420b64cd90.png)
 

## Edit a project and delete a project

### Edit a project

If you need to modify the name of the created project, you can find the project you need to modify in the project list on the left, and click the "modify icon" to modify the project name and description.

![EMQX Cloud Edit a project](https://assets.emqx.com/images/7969265c0b6d94bd328244cbecaeeb02.png)

### Delete a project

If you need to delete a project, you can click the "delete icon" to delete the project.

![EMQX Cloud Delete a project](https://assets.emqx.com/images/86d08bd07fc38354922d9343fff69624.png)
 

In the future version, EMQX cloud will further support project-based user permission management to truly grant different operation permissions to different roles.

If you have any comments or questions about our products and services, please send an email to [cloud-support@emqx.io](mailto:cloud-support@emqx.io), and our team will provide you with a one-on-one consultation service.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
