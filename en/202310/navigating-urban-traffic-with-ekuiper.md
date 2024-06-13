Real-time data is becoming a cornerstone in urban planning and traffic management, offering insights that can significantly improve daily commutes. Imagine the frustration of walking to a bike-sharing station, only to find all the bikes are taken or, conversely, no slots available to park your bike. With tools like eKuiper and datasets like CityBikes, we're about to change that narrative. Let's dive in.

## **eKuiper: Real-Time Data Analysis at the Edge**

Our journey of personal traffic analysis starts with an open-source tool: [eKuiper](https://ekuiper.org/). Initiated by [EMQX](https://github.com/emqx/emqx), this open-source marvel is not just lightweight and scalable but also boasts powerful edge computing capabilities. Its SQL-like syntax ensures that even those with a rudimentary understanding of data querying can harness its power. For traffic enthusiasts, eKuiper's real-time data processing provides a granular understanding of road conditions.

## **Getting Started with eKuiper**

To harness eKuiper's capabilities, we first need to set it up. Here's a simplified guide:

### Install eKuiper

To install eKuiper, follow the official [installation guide](https://ekuiper.org/docs/en/latest/installation.html). For this tutorial, we'll use Docker deployment, suitable for most users:

```
docker pull lfedge/ekuiper:latest
docker run -p 9081:9081 -d --name kuiper -e MQTT_SOURCE__DEFAULT__SERVER="tcp://broker.emqx.io:1883" lfedge/ekuiper:latest
```

### Preparing the Datasource in eKuiper

The first step in personal traffic analysis is acquiring the necessary data. With eKuiper's HTTP Pull Source, we can tap into open platforms offering real-time traffic data. In this tutorial, we will use the data from [CityBikes API dataset](https://api.citybik.es/v2/) as an example to demonstrate how to fetch the corresponding API data using eKuiper for further processing.

After some preliminary analysis, we found this dataset provides rich shared-bike data for London and `santander-cycles` is the major player there, so we will focus on this operator. 

The URL and parameters of the data interface are as follows:

```
http://api.citybik.es/v2/networks/santander-cycles
```

By observing the data returned from the API, we can see that all the data we need is in the array field called `stations`:

```
"network": {
        "company": [
            "PBSC",
            "Serco Group plc"
        ],
        "href": "/v2/networks/santander-cycles",
        "id": "santander-cycles",
        "location": {
            "city": "London",
            "country": "GB",
            "latitude": 51.51121389999999,
            "longitude": -0.1198244
        },
        "name": "Santander Cycles",
        "stations": [
            {
                "empty_slots": 15,
                "extra": {
                    "installDate": "1278947280000",
                    "installed": true,
                    "locked": false,
                    "name": "River Street , Clerkenwell",
                    "removalDate": "",
                    "temporary": false,
                    "terminalName": "001023",
                    "uid": 1
                },
                "free_bikes": 4,
                "id": "7f3020118e56165ed8b2f61899edb971",
                "latitude": 51.52916347,
                "longitude": -0.109970527,
                "name": "001023 - River Street , Clerkenwell",
                "timestamp": "2023-08-22T06:54:35.118000Z"
            },
        ]    
        ...
}
```

And this is the explanation of each station field:

| **Field**   | **Description**                                   |
| :---------- | :------------------------------------------------ |
| empty_slots | Number of empty slots available at the station.   |
| free_bikes  | Number of available bikes at the station.         |
| id          | A unique identifier for the station.              |
| latitude    | Geographical latitude coordinate of the station.  |
| longitude   | Geographical longitude coordinate of the station. |
| name        | Name of the station.                              |
| timestamp   | The timestamp of the last update.                 |

Now let's try to use the HTTP Pull Source of eKuiper to fetch the message data from the data platform's HTTP server and input it into the eKuiper processing pipeline.

The data preparation in eKuiper can be divided into 2 steps: first configure the HTTP pull stream and then create the HTTP pull stream with the configuration. 

### Configuring the HTTP Pull Stream in eKuiper

Once installed, eKuiper needs to be configured to pull data from the desired source, in this case, the CityBikes API. This involves setting up the HTTP Pull Source with the correct endpoint and parameters.

1. **Access the Configuration File**: Navigate to the eKuiper directory where the configuration files are stored. Locate the `httppull.yaml` file in the `etc/sources/` directory.

2. **Edit the Configuration File**: Open the `httppull.yaml` file in a text editor of your choice.

3. **Update the Configuration**: Replace the content of the file with the provided configuration. This configuration sets up a recurring API request to the Santander Cycles API every 10 seconds. It requests JSON data, requires no SSL verification, and handles the response as code.

   ```
   default:
     url: 'http://api.citybik.es/v2/networks/santander-cycles'
     method: get
     interval: 10000
     timeout: 5000
     incremental: false
     body: ''
     bodyType: json
     insecureSkipVerify: true
     headers:
       Accept: application/json
     responseType: code
   ```

1. Save the changes.

### Creating the STREAM in eKuiper

This section uses Postman for interacting with eKuiper.

1. **Open Postman**: Launch the Postman application on your computer.

2. **Set Up the Request**:

   - **HTTP Method**: Select `POST` from the dropdown menu.
   - **URL**: Enter the eKuiper API endpoint. Replace `{{host}}` with the actual host address where eKuiper is running, e.g., `http://localhost:9081/streams`.

3. **Configure Headers**: Click on the `Headers` tab and set the `Content-Type` to `application/json`.

4. **Enter the Request Body**: Click on the `Body` tab, select `raw`, and paste the following JSON:

   ```
   {
     "sql": "CREATE STREAM citybike_data () WITH (TYPE=\"httppull\")"
   }
   ```

   > Note, we will not define the data schema at this stage.

1. **Send the Request**: Click on the `Send` button to create the STREAM in eKuiper.
2. **Review the Response**: After sending the request, you should receive a response from eKuiper, in this case, “Stream citybike_data is created” is returned. 

To ensure that the STREAM was created successfully and is fetching data, you can **check eKuiper Logs**  or use an HTTP GET request to verify the stream's creation status, in this case:

```
### HTTP GET
http://localhost:9081/streams/citybike_data
```

Using eKuiper's HTTP Pull Source, we can continuously fetch data from CityBikes. This data then enters eKuiper's processing pipeline where it can be analyzed, filtered, and acted upon in real-time.

### Data Pre-Processing

Data preprocessing is a crucial step in real-time data analysis. Ensuring that the data is in the right format and structure can significantly impact the accuracy and efficiency of the analysis. As we observed from the previous steps, the `stations` field is an array within the network, as we want to perform calculations and processing using the `UNNEST` to return the data from the array as multiple rows. 

#### UNNEST the ARRAY Data

1. **Set Up the Request**:

   - **HTTP Method**: Select `POST` from the dropdown menu.
   - **URL**: Enter the eKuiper API endpoint. Replace `{{host}}` with the actual host address where eKuiper is running, e.g., `http://localhost:9081/rules`.

2. **Configure Headers**: Click on the `Headers` tab and set the `Content-Type` to `application/json`.

3. **Enter the Request Body**: Click on the `Body` tab, select `raw`, and paste the following. With this request, we will return the `stations` array data as multiple rows and also add a new memory target/source with the `actions` field. 

   ```
   {
     "id": "unnest_station_array",
     "sql": "SELECT unnest(network.stations) FROM citybike_data",
     "actions": [{
       "log": {
       },
       "memory": {
         "topic": "channel/data"
       }
     }]
   }
   ```

4. **Send the Request**: Click on the `Send` button to create the RULE in eKuiper.

5. **Review the Response**: After sending the request, you should receive a response from eKuiper, in this case, “Rule unnest_station_array was created successfully” is returned. 

#### Create a Memory Stream 

We can employ the [Memory Source](https://ekuiper.org/docs/en/latest/guide/sources/builtin/memory.html) to integrate the results of a prior rule into succeeding rules, thereby establishing a rule pipeline for systematically handling data generated by the preceding rule.

```
###
POST http://{{host}}/streams
Content-Type: application/json

{"sql": "create stream citybike_data_flatten () WITH (DATASOURCE=\"channel/data\", FORMAT=\"JSON\", TYPE=\"memory\")"}
```

Now the data is flattened and we can continue our exploration with the data. 

## **Deeper Dive into Bike Availability**

With the data ready, we can analyze the data to identify patterns related to bike availability. We want to focus on bike availability insights.

Being able to anticipate the availability of bikes ensures that we can rely on the service for our daily routines or unplanned trips.

We can calculate the bike availability at each station and then forward the analysis result to a [public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker), for example, `broker.emqx.io:1883`. 

```
{
  "id": "bike_availability",
  "sql": "SELECT name, (free_bikes / (empty_slots + free_bikes)) AS availability FROM citybike_data_flatten WHERE (empty_slots + free_bikes)!= 0",
  "actions": [{
    "log": {
    },
    "mqtt": {
        "server": "broker.emqx.io:1883",
        "topic": "bike/availability",
        "protocolVersion": "3.1.1",
        "qos": 0,
        "retained": false
      }
  }]
}
```

You can check the running status of your rule with the following command

- **HTTP Method**: Select `GET` from the dropdown menu.
- **URL**: Enter the eKuiper API endpoint. Replace `{{host}}` with the actual host address where eKuiper is running, e.g., `http://localhost:9081/rules/rulesID/status`, in this case `http://localhost:9081/rules/`station_proximity_rule`/status`

### View the Bike Availability Insight

Then we can use an MQTT client tool to subscribe to the topic and view the analyzed data, for example, [MQTTX](https://mqttx.app/). 

Launch MQTTX, click **Add a New Connection**, and set it as follows, then click the **Connect** button to build the connection. 

![Add a New Connection](https://assets.emqx.com/images/14d1f8cde8be20b173aa3ccef85bac42.png)

Click **+ New Subscription** and subscribe to the topic we just created. 

![New Subscription](https://assets.emqx.com/images/be4981c31012f770054d56f840454194.png)

Then you will be able to see the returned availability information and the site name 

![returned availability information](https://assets.emqx.com/images/7df6fc37dfdd745cee6abf826c6c4694.png)

## **Further Explorations with eKuiper**

Every commuter is unique. With eKuiper, you can:

- **Create User Profiles**: Understand and cater to individual commuting patterns. For example, let eKuiper locate the nearest top 10 shared bike stations. 
- **Set Custom Alerts**: Stay updated on your favorite stations or routes. For example, let eKuiper only return the stations with over 80% of bikes available. 

For those interested in diving deeper into eKuiper's capabilities, the [official documentation](https://ekuiper.org/docs/en/latest/) is a great place to start. The community forums are also a valuable resource for discussions and troubleshooting.

## **Conclusion: Revolutionizing Urban Commutes**

In the urban jungle, the right information can transform your daily commute from a chore to a breeze. With eKuiper, that transformation is not just possible—it's here. Ready to redefine your commute? Try eKuiper and share your experiences and results with us on [Twitter](https://twitter.com/EMQTech) or [LinkedIn](https://www.linkedin.com/company/emqtech).



<section class="promotion">
    <div>
        Try eKuiper for Free
    </div>
    <a href="https://ekuiper.org/downloads" class="button is-gradient px-5">Get Started →</a>
</section>
