## What Is MQTT on Docker?

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) is a lightweight messaging protocol designed for low-bandwidth, high-latency networks. Docker is an open-source platform that allows you to automate the deployment, scaling, and management of applications within containers. So, when you run MQTT on Docker, you are deploying the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) within a Docker container.

This combination provides a scalable and reliable solution to handle data streams in real-time, particularly in IoT applications. The MQTT broker receives messages from publishers (devices or applications that produce data) and dispatches them to subscribers (devices or applications that consume data). By running the broker on Docker, you can make it easier to deploy and scale your MQTT broker.

We’ll show how to deploy MQTT on Docker with [EMQX](https://www.emqx.io/), a popular, open source MQTT broker. EMQX provides powerful capabilities not available in other open source brokers, such as clustering, persistence, and support for very large scale deployments.

## Why Should You Run an MQTT Broker on Docker?

Running an MQTT broker on Docker provides several advantages.

- **Rapid deployment:** Docker containers can be started in a matter of seconds, which means your MQTT broker can be up and running quickly.
- **Isolation:** Docker containers run in isolation from each other, ensuring that the broker's processes do not interfere with each other or with the host system. This lets you run multiple instances of the MQTT broker on the same host without any conflicts.
- **Scalability:** Docker allows you to scale your MQTT broker horizontally (by adding more containers) or vertically (by adding more resources to a container). This scalability allows you to handle larger data or transaction volumes. You can automate scalability for large deployments with an orchestrator like Kubernetes (read our guide to [MQTT with Kubernetes](https://www.emqx.com/en/blog/running-mqtt-on-kubernetes)).
- **Portability:** Docker containers can run on any system that has Docker installed, regardless of the underlying operating system. This means you can build your MQTT broker on your local system, test it, and then deploy it reliably on any cloud or on-premise server.

## Setting Up an MQTT Broker in Docker with Clustering and Persistence 

EMQX is the leading open source MQTT broker. It provides a Docker Official Image which is [available on Docker Hub](https://hub.docker.com/_/emqx).

A major advantage of EMQX is that it **supports clustering** for large scale MQTT deployments. Most other articles on this topic show how to set up the [Mosquitto MQTT broker](https://www.emqx.com/en/blog/mosquitto-mqtt-broker-pros-cons-tutorial-and-modern-alternatives) with Docker - but Mosquitto does not support clustering. Additional EMQX features include:

- Ability to scale up to 100M+ IoT devices in 1 cluster, while maintaining 1M message per second throughput and sub-millisecond latency.
- 100% compliant with MQTT 5.0 and 3.x, support for multiple open standard protocols like HTTP, [QUIC](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov), and WebSocket.
- Secures bi-directional communication with MQTT over TLS/SSL and various authentication mechanisms.
- Uses powerful SQL-based rules engine to extract, filter, enrich and transform IoT data in real-time.
- Ensures high availability and horizontal scalability with a masterless distributed architecture.
- More than 20K+ enterprise users across 50+ countries and regions, connecting 100M+ IoT devices worldwide. Trusted by over 400 customers in mission-critical scenarios including over 70 Fortune 500 companies.

Here is how to use the EMQX Docker image to quickly get up and running with MQTT.

### Install Docker

To install Docker, open a terminal window and install Docker using the appropriate command for your operating system. If you're using Ubuntu, for example, you'd use the following command:

```
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io 
```

Once the installation is complete, you can confirm that Docker is running by typing:

```
sudo systemctl status docker
```

The output should look like this:

![Install Docker](https://assets.emqx.com/images/0699c3d497f6767aa69cdbe131ada712.png)

If everything is set up correctly, you should see Docker listed as active (running).

### Pull the EMQX Broker Image

To get started with EMQX, the first step is to download the EMQX Docker image from Docker Hub. Open your terminal and run the following command:

```
docker pull emqx:latest
```

This command fetches the latest EMQX broker image and prepares it for use on your machine.

### Run the EMQX Broker Image

After pulling the image, you can start a new EMQX container. Use the following command to run the EMQX Docker image:

```
docker run -d --name emqx -p 18083:18083 -p 1883:1883 emqx:latest
```

We can check if the container is running by executing the docker ps command. The output should look like this:

![Run the EMQX Broker Image](https://assets.emqx.com/images/ab07ef39d2d8fab37fb1b14571ee81e8.png)

Here, the -d flag runs the container in detached mode. Ports 18083 and 1883 are mapped to your host machine, allowing you to interact with the EMQX broker. The EMQX broker runs as the Linux user emqx inside the container.

### Set MQTT Configuration

You can set configurations via environment variables when running your Docker container. All EMQX settings in etc/emqx.conf can be configured this way (to learn about EMQX configuration options, refer to the [official documentation](https://www.emqx.io/docs/en/v5.0/configuration/configuration-manual.html)).

Environment variables with the prefix EMQX_ map to key-value pairs in the configuration files. For example, here's how to set the MQTT TCP port to 1883:

```
docker run -d --name emqx -e EMQX_LISTENERS__TCP__DEFAULT__BIND=1883 -p 18083:18083 -p 1883:1883 emqx:latest
```

In this example, EMQX_LISTENERS__TCP__DEFAULT__BIND=1883 sets the MQTT TCP port to 1883. The -e flag specifies the environment variable.

### Set Up Clustering

Before proceeding with this step, please ensure docker-compose is installed on your system.

For clustering, you can create a `docker-compose.yaml` file as follows:

```
version: '3'
services:
  emqx1:
    image: emqx:latest
    container_name: emqx1
    environment:
      - "EMQX_NAME=emqx1"
      - "EMQX_HOST=emqx1.emqx.io"
      - "EMQX_CLUSTER__DISCOVERY_STRATEGY=dns"
      - "EMQX_CLUSTER__DNS__RESOLVER=8.8.8.8"
      - "EMQX_CLUSTER__DNS__INTERVAL=5000"
    networks:
      emqx-net:
        aliases:
          - emqx1.emqx.io
    ports:
      - "1883:1883"
      - "8083:8083"

  emqx2:
    image: emqx:latest
    container_name: emqx2
    environment:
      - "EMQX_NAME=emqx2"
      - "EMQX_HOST=emqx2.emqx.io"
      - "EMQX_CLUSTER__DISCOVERY_STRATEGY=dns"
      - "EMQX_CLUSTER__DNS__RESOLVER=8.8.8.8"
      - "EMQX_CLUSTER__DNS__INTERVAL=5000"
    networks:
      emqx-net:
        aliases:
          - emqx2.emqx.io
    ports:
      - "1884:1883"
      - "8084:8083"

networks:
  emqx-net:
    driver: bridge
```

Then run the cluster with this command:

```
docker-compose -p my_emqx up -d
```

To view the cluster status, run:

```
docker exec -it emqx1 sh -c "emqx_ctl cluster status"
```

The output should look like this:

![The output](https://assets.emqx.com/images/026cb15ffb81ed815fabe719fa9150af.png)

### Set Up Persistence

To persist container data, EMQX requires the following directories to be saved:

- /opt/emqx/data
- /opt/emqx/etc
- /opt/emqx/log

To make these directories persistent, use volume mounts in your `docker-compose.yaml` file like so:

```
services:
  emqx:
    # ... previous configurations
    volumes:
      - vol-emqx-data:/opt/emqx/data
      - vol-emqx-etc:/opt/emqx/etc
      - vol-emqx-log:/opt/emqx/log
```

The output should look something like:

![docker compose up](https://assets.emqx.com/images/31bda0c26dd7fdabb281e8c03f003dfd.png)

To ensure the same state when the container restarts, make sure to specify the `EMQX_NAME` and `EMQX_HOST` variables as previously defined.

## Large-Scale MQTT Deployment with EMQX

Running MQTT on Docker offers several compelling advantages, including rapid deployment, isolation, scalability, and portability. Leveraging Docker containers for MQTT deployment allows for efficient resource utilization and ease of management.

For those looking to set up MQTT on Docker with clustering and persistence, EMQX proves to be a powerful choice. EMQX's support for clustering, compliance with MQTT standards, and advanced features make it suitable for large-scale MQTT deployments.

Read these blog posts to see how to massively scale up MQTT with EMQX:

- [Reaching 100M MQTT connections with EMQX 5.0](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0)
- [How EMQX with the Mria + RLOG architecture achieves 100M MQTT connections](https://www.emqx.com/en/blog/how-emqx-5-0-achieves-100-million-mqtt-connectio)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
