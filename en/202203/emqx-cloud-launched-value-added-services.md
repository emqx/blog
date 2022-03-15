[EMQX Cloud](https://www.emqx.com/en/cloud) is committed to providing reliable and efficient fully managed MQTT message cloud services for customers of different scales and industries. Through this easy-to-use and standardized SaaS product, users can freely build IoT applications like “Lego”.

Facing the different personalized needs of customers, the EMQX Cloud team decided to set up a new value-added feature section based on the original product form to provide users with more high-value functions. Users will be able to choose value-added services according to their needs, saving unnecessary costs.

## Two value-added features are newly opened

The two newly-opened value-added features are the internal load balancer and NAT gateway, both provide a 14-day free trial.

### Internal load balancer

Internal load balancer is a service that distributes traffic on-demand in the intranet. It can extend the throughput capacity of applications by distributing traffic to different back-end servers, and improve the availability of applications by eliminating single points of failure in the system.

### NAT gateway

The NAT gateway offers network address translation services, which can provide the ability to access public network resources without the need for VPC peer-to-peer connectivity.

> Note: Two features are only avaliable in the professional version.

## How to subscribe

Log in to the EMQX Cloud Dashboard, go to the top menu bar -> Value-added services(VAS)

![EMQX Cloud Value-added services](https://static.emqx.net/images/2f8cba96b9a99b612a7e07b072a29ef2.png)
 
or Subscribe designated value-added services at the bottom of the deployment overview

![EMQX Cloud Dashboard](https://static.emqx.net/images/d97195c9759473d9d6a27280788bac16.png)
 
Click Subscribe Now, drop down to select the deployment to be bound to the value-added service, and click Next

![EMQX Cloud Dashboard](https://static.emqx.net/images/e480c9a6f4d416003cfb08beae7dd228.png)
 
Confirm the service information and click Buy Now to confirm the purchase

![EMQX Cloud Dashboard](https://static.emqx.net/images/0bab7dc3132b6d87af01d0f4fd190b25.png) 

Click Go to Services to start configuring the use of value-added services.

> Note: The deployment of different versions only displays the value-added services that can be used and activated in the deployment of this version.

 
## Pricing method

After the NAT gateway and internal load balancer are activated, you will automatically get a 14-day free trial. After the first trial instance ends or is deleted, the next instance created will be charged.

After the trial is over, the NAT gateway and internal load balancer features will be billed at $0.1/hour and $0.05/hour respectively, and will be billed hourly from the account balance under your EMQX Cloud master account. If the account balance is insufficient, the value-added service will be automatically deleted.

The details of expenses can be viewed in Financial Management -> Overview -> Hourly Bills and Historical Bills to view the deduction details.

> Note: When the deployment of the value-added service is stopped, the non-trial value-added service will be billed normally. To avoid additional charges, please delete the value-added services under this deployment.

## Configuration instructions

### Internal load balancer configuration

After completing the purchase of the internal load balancer service, you can view the creation status of it  in the corresponding deployment overview, and wait for the creation to complete.

![EMQX Cloud Internal load balancer configuration](https://static.emqx.net/images/a28b0069e5e73ff37de1cc868e703981.png)
 

When the status of the internal load balancer is running, you can connect the terminal under the VPC that has completed the peering connection to the deployment through the intranet IP of the intranet address. The connection port is the same as the public network connection port: mqtt port is 1883, websocket The port is 8083.

### NAT gateway configuration

After completing the purchase of the NAT gateway value-added service, you can see the NAT gateway creation status in the corresponding deployment overview, and wait for the creation to complete.

![EMQX Cloud NAT gateway configuration](https://static.emqx.net/images/6e54bcdec555edfd52cd2cb7538c5339.png)
 

When the status of the NAT gateway is running, the deployment can access public network resources.

 

The EMQX Cloud team will continue to collect user needs and launch more value-added services based on that. If you have any requirements, please let us know.
