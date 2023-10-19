For decades, OpenWRT has remained the most popular Linux operating system targeting embedded devices. As a fully customizable operating system for wireless routers, OpenWRT frees you from the application selection and configuration without vendor lock-in. For developers, it is easier and more friendly to build an application without building complete firmware around it.

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is the de facto standard protocol for IoT applications. With an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) set up in OpenWRT routers and operating as a local IoT server, it would unlock the edge computing capability and enable your own IoT applications. In the past, [Mosquitto](https://www.emqx.com/en/blog/mosquitto-mqtt-broker-pros-cons-tutorial-and-modern-alternatives) was the only choice of edge MQTT broker on OpenWRT. In this blog, we will provide a new solution to running MQTT on OpenWRT with NanoMQ. The better scalability and integrations make it a perfect alternative to Mosquitto.

## What is NanoMQ?

[NanoMQ](https://nanomq.io/) ([github.com/emqx/nanomq](https://github.com/emqx/nanomq)) is a lightweight and high-performance MQTT broker and messaging bus for edge computing, which unifies data in motion and data at rest. With its elegant and powerful design, users could achieve a high level of time and space efficiency while enjoying portability and scalability when accessing the data on edge.

For more information about NanoMQ, please check [https://nanomq.io/](https://nanomq.io/).

## Prerequisites

- OpenWRT 19.07 (21.02 is recommended) environment
- OpenWRT build system
- NanoMQ (0.6.6 or above)
- CMake (3.13 or above)
- Optional: OpenWRT SDK/Toolchain (alternative to build system)

OpenWRT build system only supports Makefile. However, the NanoMQ project is built via CMake. Hence, we will perform a cross-compile to port NanoMQ to OpenWRT.

## Download the Source Code of NanoMQ

Download the source of NanoMQ from [https://github.com/emqx/nanomq](https://github.com/emqx/nanomq). Compared to Mosquitto, NanoMQ also provides more awesome features other than MQTT server, such as HTTP REST API, ZeroMQ & nanomsg proxy, event webhook, and Offline data cache in SQLite3. Please adjust the build settings according to your requirements. But be aware that TLS/SSL encryption and SQLite3 will bring in new dependencies, which are not included in this tutorial.

```
git clone https://github.com/emqx/nanomq.git ; cd nanomq
git submodule update --init --recursive
```

Please try to compile NanoMQ on the host to verify the source code :

```
mkdir build && cd build
cmake .. 
make
```

## Install OpenWRT Build System.

Now we’ve got NanoMQ ready, then it is time to prepare OpenWRT build system. Please refer to the official guidance here: [Build system setup](https://openwrt.org/docs/guide-developer/toolchain/install-buildsystem). Take Ubuntu as an example:

```
# Install Prerequisites
$ sudo apt install build-essential subversion git-core libncurses5-dev zlib1g-dev gawk flex quilt libssl-dev xsltproc libxml-parser-perl mercurial bzr ecj cvs unzip

# Download and update the sources
git clone https://git.openwrt.org/openwrt/openwrt.git
cd openwrt
git pull
 
# Update the feeds
./scripts/feeds update -a
./scripts/feeds install -a

# Adjust OpenWRT image
make menuconfig
```

## Import NanoMQ Project to OpenWRT

In this step, we import NanoMQ as a package of OpenWRT. Firstly, create an independent folder 'emqx/nanomq/src' in the 'package' path of OpenWRT, and copy the source code of NanoMQ we downloaded previously to the src/ directory as below:

```
package/
├── ...
└── emqx/
    ├── ...
    └── nanomq/
        ├── Makefile (new file)
        └── src/
            ├── CMakeLists.txt
            ├── deploy/
            ├── docs/
            ├── nanomq/
            ├── nanolib/
            ├── nng/
            └── ...
```

## Compose Makefile for NanoMQ

You may have noticed that we created a new Makefile in the nanomq folder. It is how the OpenWRT knows where to find NanoMQ. Please edit the Makefile as below:

```
include $(TOPDIR)/rules.mk

PKG_NAME:=nanomq
PKG_VERSION:=0.6.6
PKG_RELEASE:=1
PKG_LICENSE:=MIT

include $(INCLUDE_DIR)/package.mk
include $(INCLUDE_DIR)/cmake.mk

define Package/nanomq
  SECTION:=net
  CATEGORY:=emqx
  TITLE:=NanoMQ Broker
  URL:=https://github.com/emqx/nanomq
  DEPENDS:=+libpthread +librt
  MAINTAINER:=NanoMQ-Team<contact@emqx.io>
endef

define Package/Prepare
  mkdir -p $(PKG_BUILD_DIR)
  $(CP) ./* $(PKG_BUILD_DIR)/
endef

define Package/nanomq/decription
  NanoMQ edge messaging bus
endef

define Package/nanomq/install
  $(INSTALL_DIR) $(1)/usr/bin
  $(INSTALL_BIN) $(PKG_BUILD_DIR)/build/nanomq/nanomq $(1)/usr/bin
endef

$(eval $(call BuildPackage,nanomq))
```

## Cross-Compile & Install NanoMQ

This is the final step, just update the feed source, select NanoMQ in the menuconfig. Then build the OpenWRT image, and NanoMQ will be compiled as well.

```
# Update the feed sources
$ ./scripts/feeds update -a
$ ./scripts/feeds install -a

# select nanomq in menuconfig
make menuconfig

# build image
$ make
```

![image.png](https://assets.emqx.com/images/793da65bf3d5c99c501c16afd5cbf040.png)

<center>Menuconfig in make</center>

<br>

Select emqx and type enter.

![NanoMQ in OpenWRT](https://assets.emqx.com/images/ad5ad604aec5b3c4ccfe04dc2789608d.png)

<center>NanoMQ in OpenWRT</center>

<br>

Press Y to include nanomq.

Or you can build NanoMQ separately. It is convenient to be able to build only the package.

```
$ make package/emqx/nanomq/compile V=s
```

After you install the OpenWRT onto your board, find the ipk in build dir and copy to your OpenWRT router. Then install it with `opkg`. The `ipk` package can be found at `bin/packages/your_arch/base/nanomq_0.6.6-1_***.ipk`.

```
$ opkg install nanomq_0.6.6-1_***.ipk
```

Start NanoMQ on OpenWRT and enjoy.

```
$ /usr/bin/nanomq broker start
```

#### Notes:

In this tutorial, we take NanoMQ 0.6.6 as an example. Please find the the most updated version of NanoMQ at [Releases · emqx/nanomq](https://github.com/emqx/nanomq/releases/). As for the newly released features such as DDS proxy and [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic) bridging is not included, only basic MQTT broker functionality is tested on OpenWRT, extra migration work is required for other parts. 

When building NanoMQ on OpenWRT, some libs can not be found.

If libc.so.6 can not be found, edit `'staging_dir/target-***/pkginfo/libc.provides'` .

```
libc.so
libc.so.6
libgcc_s.so.1
```

If libpthread can not be found, edit `'staging_dir/target-***/pkginfo/libpthread.provides'` .

```
libpthread.so.0
libgcc_s.so.1
```

If librt can not be found, edit `'staging_dir/target-***/pkginfo/librt.provides'` .

```
librt.so.1
libgcc_s.so.1
```

## Conclusion

NanoMQ, as a popular open-sourced, lightweight MQTT broker and edge messaging bus, is widely used in IoT/IIoT (Industrial Internet of Things) and SDV (software-defined vehicle) scenarios. By porting NanoMQ to the OpenWRT, making NanoMQ + OpenWRT a cost-effective combo solution for the community. It expands the boundary of both open-source projects, and users could get more options while building the solution.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
