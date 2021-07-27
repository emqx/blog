Recently, [EMQ](https://www.emqx.com/en) sponsored the open source project Vue.js through the Open Collective platform. In the future, EMQ will continue to provide regular sponsors to this JavaScript framework which is widely used in the field of front-end development, to support the benign operation of the project, and continue to provide convenient and efficient front-end development methods for global developers.

[Vue.js](https://vuejs.org/) is a progressive JavaScript framework for building user interfaces. The author Evan You first released and open-sourced this framework in February 2014. Nowadays, it is the most popular front-end development framework. At present, there are 185K Stars and nearly 2 million downloads per month on GitHub. Unlike other large frameworks, Vue is designed to be applied layer by layer from the bottom up. The core library of Vue.js only focuses on the view layer, which is not only easy to use, but also easy to integrate with third-party libraries or existing projects.

EMQ has a long history with vue.js. In 2013, EMQ's open source project was released on GitHub. With the increase in the number of users and the emergence of enterprise-level requirements, higher requirements have been put forward for graphical interface operations and website quality.  For this reason, EMQ has successively used Vue.js to develop products, documents, and official websites. Today, EMQ's core product [EMQ X](https://www.emqx.com/en/products/emqx) has become an MQTT message server widely used in the global market. Behind the increasingly complete products and projects, we have got a lot of support from the Vue.js project.



## EMQ & Vue.js

### Dashboard

EMQ X open source MQTT broker has powerful performance and complete functions. In order to allow users to use EMQ X more intuitively and conveniently, we also provide a complete graphical interface, namely EMQ X Dashboard. The Dashboard is built on the Vue.js open-source project. Thanks to the many features of Vue, we can quickly and completely build such an excellent graphical interface to meet the needs of users and help users improve development and usage efficiency.

For example, based on the data-driven-rendering feature of Vue, our Dashboard allows users to quickly and conveniently view various real-time indicator data and their changes without having to refresh the entire page each time. Based on the feature of the simple component implementation, We can quickly reuse the same functions on each page so that users can quickly complete the SQL writing of the rule engine in the Dashboard with some third-party components.

![EMQ X Dashboard](https://static.emqx.net/images/828187dfa5ed98b512f47c7ba4d90a99.png)      

### Document

In addition to function development, we also implemented a relatively complete [EMQ X document site](https://docs.emqx.io/) by using Vue. The document is an important part of the entire product and content presentation. A good product is inseparable from a good document. After comparing and investigating various document frameworks and tools, we finally decided to use [VuePress](https://vuepress.vuejs.org), a minimalistic Vue-powered static site generator, to develop an online site for EMQ X documents, which provides users with convenient, fast, and efficient document access and entry.

![EMQ X Document](https://static.emqx.net/images/82862232417b9e6701e2f2f874275040.png)       

### Website

In the previous development of the [EMQ website](https://www.emqx.com/en), we have always used the traditional HTML + JQuery tech stack to program the official website, which is relatively complex and inefficient. In order to improve development efficiency and take account of SEO, we chose [Nuxt.js](https://nuxtjs.org)(a server-side rendering application framework based on Vue.js) in the subsequent website development, which can also generate static sites. This allows us to complete website development by writing the familiar Vue.js single-file component, which makes us experience all the features of Vue.js and also get help in SEO.

![EMQ Website](https://static.emqx.net/images/66910c01e59b64557be5eb54c9fd0fae.jpg)

### Tool

In addition to the above-mentioned integration of Vue.js and various applications of EMQ, we also use Vue.js to develop a developer tool with GUI (graphical user interface) features, a cross-platform MQTT 5.0 desktop client tool developed based on Vue.js + Electron - [MQTT X](https://mqttx.app). It is convenient for users to use graphical functions to quickly develop and debug [MQTT Broker](https://www.emqx.io). In the development of MQTT X, we have taken advantage of many capabilities of Vue.js to bring convenience to more users and developers through such application tools.

![MQTT X](https://static.emqx.net/images/850e0b06a597388c49204a731b9dd098.png)

## Helping open source

All along, we would like to express our heartfelt thanks to the vue.js open-source project and its authors. As the sponsor and operator of an open-source project, we are well aware of the difficulty of maintaining an open-source project. Nowadays, although open source projects are blooming everywhere, to maintain stable and healthy operations and continue to bring value to the community, project maintainers need to pay more energy and even financial investment than we thought. In fact, many of the projects that have received much attention were abandoned by the original author due to various reasons in the later period, and fell into a state of no dedicated maintenance. This is a pity for the open source field.

EMQ believes that for open source projects, especially individual's open source projects, in addition to community recognition and code contributions, financial support is also an important way to encourage project maintainers. Evan You, the author of the Vue.js project, also mentioned that although the original intention of open source is not to get returns, the project maintainer also needs enough recognition and support to get the motivation and significance of persistence. At the same time, it can encourage more developers to join in open source and make the open source ecology develop healthily. Therefore, we decided to become a regular donor of the Vue.js project, hoping to contribute to its future development.

With the emergence of collaborative production method between open source and community, it has reduced a lot of 「repetitive wheel building」work and greatly improved work efficiency in the whole industry, and this positive impact is extensible. Just as EMQ develops the user interface layer with the help of vue.js open source framework, our users will use the EMQ X open source MQTT Broker to build the underlying IoT platform, and the next level of our users will get more application services through the IoT platform they provide. In this way, various industries obtain technology and capability sharing and collaboration through open source, and the entire human society will achieve efficient and positive development. This is the meaning of open source.

We believe that with more and more support, the open source ecosystem will be more prosperous. EMQ will work with many excellent open source projects and companies to 「To serve the future of the human industry and society through world-class open source software」.
