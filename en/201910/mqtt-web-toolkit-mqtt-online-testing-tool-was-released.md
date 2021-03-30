The MQTT Web Toolkit is a recently open source MQTT (WebSocket) testing tool from EMQ that supports online access ([tools.emqx.io](http://tools.emqx.io)). The tool adopts the form of chat interface, simplifies the page operation logic, and facilitates users to test and verify MQTT application scenarios quickly.

#### Function introduction

1. Support to connect to the MQTT broker through a normal or encrypted WebSocket port;
2. The links are created, edited, deleted and cached to facilitate the next visit;
3. Subscription list management for different links;
4. Prompt when the message is published, received and new message is received, and also support filtering message list by message type.

#### Guide for use

##### Create/delete links

Use the browser to open the address [tools.emqx.io] (http://tools.emqx.io), click the **New Connection** button in the lower left corner, and enter the link information to create a link in the pop-up box.

When the mouse **Hover**  to an item in the list of links on the left, the deletion icon is displayed. Clicking on the icon to delete the link.

![image20190929144601696.png](https://static.emqx.net/images/d9fa323d46085d81f292d9e3317bde2b.png)

##### Subscription management

Once the link is created, click the **Connect** button in the top right corner to connect to the MQTT server. After the connection is successful, click the **New Sub** button in the upper left corner to pop up the subscription list box, where the New/unsubscribe operation can be performed on this page.

![image20190929144850583.png](https://static.emqx.net/images/ecfb7fa09688a8fa67af48ce54170d74.png)

##### Message Publishing/Receiving

Click the input box at the bottom right of the page to pop up the message publishing box, fill in the **Topic** and **Payload** fields and click the publish icon in the lower right corner to publish the message. After the successful publishing, the message will be displayed in the right side of the message list.

The message received with the subscription topic will be displayed on the left side of the message list. Click the message type switch button in the upper right corner to display only received or sent messages (all messages are displayed by default).

![image20190929145053171.png](https://static.emqx.net/images/cdfb57334ec49abe966be483f7cc7de6.png)



Welcome to visit [tools.emqx.io](http://tools.emqx.io) for a trial online.



------

Welcome to our open source project [github.com/emqx/emqx](http://github.com/emqx/emqx). Please visit the [official documentation](https://docs.emqx.io) for details.