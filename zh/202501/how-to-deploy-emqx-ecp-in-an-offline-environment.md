EMQX ECP 是一款工业互联数据平台，能够满足工业场景大规模数据采集、处理和存储分析的需求，提供边缘服务的快速部署、远程操作和集中管理等功能，助力工业领域数据互联互通，以数据 + AI 驱动生产监测、控制和决策，实现智能化生产，提高效率、质量和可持续性。

在当今的企业级应用部署中，EMQX ECP 提供了灵活的安装选项，如：通过 Docker Compose 和 Helm Chart 两种主流方式安装。然而，在某些特殊环境下，由于网络限制，用户无法直接访问外网，这对于依赖在线拉取 Docker 镜像的安装流程来说是一个挑战。

为了克服这一限制，EMQX 特别提供了一种离线安装 ECP 的解决方案。通过提前将所需的 Docker 镜像导入到客户的环境中，即使在没有外网连接的情况下，也能确保 ECP 的顺利部署和运行。这种离线安装方法不仅提高了安装的灵活性，还增强了在各种网络环境下的适应性和可靠性。

## docker compose 安装

1. 下载 docker image 压缩包，您也可以[联系我们](https://www.emqx.com/zh/contact?product=emqx-ecp)，获取离线安装包。

1. 解压缩

   ```shell
   mkdir  image
   tar -zxvf   emqx-ecp-dependency-images-2.4.1-alpha.4.tar.gz -C  ./image
   ```

2. 导入docker image

   ```shell
   cd image 
   for t in *.image; do docker load -i "$t"; done
   ```

3. 将下载的安装包 [emqx-ecp-docker-compose-installer-2.1.1.tar.gz](https://www.emqx.com/zh/downloads/emqx-ecp/2.4.0/emqx-ecp-docker-compose-installer-2.4.0.tar.gz) 上传到服务器上，解压缩后，进入解压缩后的目录，执行以下步骤完成 ECP 的安装。

   1）配置

   ```shell
   ./emqx_ecp_ctl configure
   ```

   ![配置](https://assets.emqx.com/images/c2206cbf6d32e71bbedca6d773beddbb.png)

   2）启动

   ```shell
   ./emqx_ecp_ctl start
   ```

   ![image.png](https://assets.emqx.com/images/8f367ee506b7d9fa89454591f056d58a.png)

   3）查看状态，全是 Up，表示安装成功

   ```shell
   ./emqx_ecp_ctl status
   ```

   ![image.png](https://assets.emqx.com/images/9c83b37322a7e6217de6493c3fa43f8f.png)

   

## helm chart 安装

1. 下载 docker image 压缩包

2. 解压缩

   ```shell
   mkdir image & tar -zxvf emqx-ecp-dependency-images-2.4.1-alpha.4.tar.gz -C  ./image
   ```

3. 导入 docker image

   在 Kubernetes 中，docker 和 containerd 的主要区别在于它们作为容器运行时的实现方式不同：docker 通过其自身的容器运行时来管理容器的生命周期，而 containerd 作为一个更轻量级的容器运行时，直接与容器交互，通常提供更简洁的接口和更好的性能。这两种导入 docker image 的方式也有所不同。

   注意：

   您可以通过以下命令来判断 Kubernetes 集群中使用的是 docker 还是 containerd：

   ```shell
   kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.containerRuntimeVersion}'
   ```

   这条命令将返回每个节点使用的容器运行时版本信息，以返回的信息是否包含「docker」或「containerd」作为判断依据。下面分别是2种情况的安装步骤：

   - **docker**

     ```shell
     cd image 
     for t in *.image; do docker load -i "$t"; done
     ```

   - **containerd**

     ```shell
     #!/bin/bash
     
     # 遍历当前文件夹下所有以 .image 结尾的文件
     for image_file in *.image; do
         # 获取不带 .image 扩展名的文件名
         base_name="${image_file%.image}"
         
         # 重命名文件，将 .image 扩展名改为 .tar.gz
         mv "$image_file" "${base_name}.tar.gz"
         
         # 解压缩 .tar.gz 文件
         gunzip "${base_name}.tar.gz"
         
         # 导入解压缩后的 .tar 文件到 containerd
         ctr -n k8s.io image import "${base_name}.tar"
         
         # 可选：删除解压缩后的 .tar 文件，以节省空间
         # rm "${base_name}.tar"
     done
     ```

     1）将上述脚本保存为一个文件，例如 `import_images.sh`。

     2）脚本执行：

     ```shell
     chmod +x import_images.sh
     ./import_images.sh
     ```

     3）查看镜像是否导入成功

     ```shell
     crictl images
     ```

4. 通过 helm chart 安装

   ```shell
   helm repo add emqx https://repos.emqx.io/charts
   helm repo update
   helm pull emqx/kube-ecp-stack --version ${version} --untar
   cd kube-ecp-stack
   ```

   如有必要， 可通过修改 `values.yaml` 来实现，比如指定使用特定的 `StorageClass`， 默认为 `standard`:

   ```yaml
   global:
      image:
         registry: ""
         repository: ""
         pullPolicy: IfNotPresent
         ##
         ## Optionally specify an array of imagePullSecrets.
         ##
         # pullSecrets: &global-image-pullSecrets
         #   - name: "ecp-registry"
         pullSecrets: &global-image-pullSecrets []
      storage:
         className: &global-storage-className "standard"
         accessModes: &global-storage-accessModes
         - ReadWriteOnce
   ```

   安装启动

   ```shell
   helm upgrade --install ${YOUR_RELEASE_NAME} . --namespace ${YOUR_NAMESPACE} --create-namespace
   ```

   大约等待30s后，检查安装的 pod 状态，如果都是 Running 状态，表示安装成功。

   ![image.png](https://assets.emqx.com/images/8701998f845f7cfeb6dde59a80cf158e.png)

   <center>查看 pod 状态</center>

## 结语

通过遵循本文提供的离线安装指南，用户可以确保 EMQX ECP 在任何环境下都能稳定运行，从而实现高效、可靠的消息队列服务。这种安装方式不仅提高了系统的可用性，还为用户提供了更多的控制权，以适应不断变化的业务需求和技术挑战。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
