##  Ingress 介绍

[Ingress](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#ingress-v1beta1-networking-k8s-io) 公开了从集群外部到集群内 [服务](https://kubernetes.io/zh/docs/concepts/services-networking/service/) 的 HTTP 和 HTTPS 路由。 流量路由由 Ingress 资源上定义的规则控制。官网的一个简单示例如下：

![ingres.png](https://assets.emqx.com/images/613a343074a20d1d246e04e7801e9bfe.png)

Ingress 为服务提供了供外部访问的 URL，负载均衡流量，TLS/SSL 终止的能力。Ingress 可以简单理解为服务的服务，通过独立的 Ingress 对象来指定请求转发的规则，将请求路由到对应的服务中。

为了让 Ingress 资源工作，集群必须有一个正在运行的 Ingress 控制器。 [NGINX Ingress Controller](https://github.com/kubernetes/ingress-nginx)  是由 Kubernetes 提供支持和维护的一个控制器。

本文主要介绍如何通过 NGINX Ingress Controller 来访问 Kubernetes 集群中的 EMQX。

## 准备

开始之前，请确保您已经搭建好了一个可用的 Kubernetes 集群，本文示例是基于阿里云标准版托管集群。

## 安装 EMQX 

参考 [emqx charts](https://github.com/emqx/emqx-rel/tree/master/deploy/charts/emqx) ，使用 Helm 进行安装

```bash
$ helm repo add emqx https://repos.emqx.io/charts
$ kubectl create ns my-emqx
$ helm install my-emqx emqx/emqx -n my-emqx
```

确保 pod 处于 running 状态

```bash
$ kubectl get pod -n my-emqx
NAME        READY   STATUS    RESTARTS   AGE
my-emqx-0   1/1     Running   0          97s
my-emqx-1   1/1     Running   0          73s
my-emqx-2   1/1     Running   0          51s
```

查看 service

```bash
$ kubectl get svc -n my-emqx
NAME               TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                                                           AGE
my-emqx            ClusterIP   172.21.5.160   <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP            5m
my-emqx-headless   ClusterIP   None           <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP,4370/TCP   5m
```

## 部署 NGINX Ingress Controller

参考 [Installation Guide](https://kubernetes.github.io/ingress-nginx/deploy/)，根据不同情况选择不同的配置进行安装，也可以通过 Helm 安装

```bash
$ helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
$ helm repo update
$ helm install my-release ingress-nginx/ingress-nginx
```

因为本文基于阿里云集群，可以直接选择组件安装

查看 service

```bash
$ Kubectl get nginx-ingress-lb svc -n kube-system
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
nginx-ingress-lb   LoadBalancer   172.21.6.205   47.99.187.164   80:30639/TCP,443:30396/TCP   3m12s
```

## 创建 Ingress 对象

```yaml
# ingress.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
  name: emqx
spec:
  rules:
  - host: emqx.cn.iotdp.cn
    http:
      paths:
      - backend:
          serviceName: my-emqx
          servicePort: 18083
        path: /
      - backend:
          serviceName: my-emqx
          servicePort: 8083
        path: /mqtt
```

路由规则：

- 匹配 `/mqtt`路由到 8083 Websocket 端口
- 其余路径路由到 18083 dashboard

部署资源

```bash
$ kubectl apply -f ingress.ymal -n my-emqx
```

部署完成以后，修改 DNS 解析，便可以通过：https://emqx.cn.iotdp.cn 来访问 dashboard

![dashboard.png](https://assets.emqx.com/images/f0b7b0ea8f5b62de1600e0178e090017.png)

然后通过 `8083` 和 `/path`访问 Websocket

![websocket.png](https://assets.emqx.com/images/f2df6fbd5827faca3020b2df4c9dd3a2.png)

## TCP

Ingress 不支支持 TCP 和 UDP 服务，因此 Ingress 使用 `--tcp-services-configmap` 和 `--udp-services-configmap` 指向一个包含端口映射关系的 `configmap` 来访问，key 为外部暴露的端口，value 格式为：`<namespace/service name>:<service port>:[PROXY]:[PROXY]`

首先修改 ingress-nginx deployment

```bash
$ kubectl edit deployment nginx-ingress-controller -n kube-system
```

添加以下内容到`spec.template.spec.containers.args`

- --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
- --udp-services-configmap=$(POD_NAMESPACE)/udp-services

```yaml
containers:
  - args:
      - /nginx-ingress-controller
      - '--configmap=$(POD_NAMESPACE)/nginx-configuration'
      - '--annotations-prefix=nginx.ingress.kubernetes.io'
      - '--publish-service=$(POD_NAMESPACE)/nginx-ingress-lb'
      - '--tcp-services-configmap=$(POD_NAMESPACE)/tcp-services'
      - '--udp-services-configmap=$(POD_NAMESPACE)/udp-services'
```

配置 `tcp-service`

```yaml
# tcp-service.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tcp-services
  namespace: ingress-nginx
data:
  1883: "my-emqx/my-emqx:1883"
```

最后在服务中配置对应端口

```bash
$ kubectl edit svc nginx-ingress-lb -n kube-system
```

配置如下

```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: nginx-ingress-lb
  name: nginx-ingress-lb
  namespace: kube-system
spec:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
      protocol: TCP
      targetPort: 80
    - name: https
      port: 443
      protocol: TCP
      targetPort: 443
    - name: emqx-tcp
      port: 1883
      protocol: TCP
      targetPort: 1883
  selector:
    app: ingress-nginx
```

查看 ingress-nginx 服务

```bash
$ kubectl get svc nginx-ingress-lb -n kube-system
NAME               TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              AGE
nginx-ingress-lb   ClusterIP   172.21.11.90   <none>        80:30639/TCP,443:30396/TCP,1883:30657/TCP   13m
```

我们便可以通过 `1883` 端口连接到 EMQX 服务了。

![mqtt.png](https://assets.emqx.com/images/869cb25e78925065dfab7bc3d9616858.png)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
