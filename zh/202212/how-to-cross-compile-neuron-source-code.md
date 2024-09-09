[Neuron](https://github.com/emqx/neuron) 是一款开源的轻量级工业协议网关软件，支持数十种工业协议的一站式设备连接、数据接入、MQTT 协议转换，为工业设备赋予工业 4.0 时代关键的物联网连接能力。

开源社区用户有时会有使用 Neuron 源码在当前编译平台下编译能够运行在体系结构不同的另一种目标平台上，即进行交叉编译的需求。在这一过程中可能会遇到由于没有安装好依赖库等原因导致的编译错误。

本文将详细介绍使用 Neuron 源码进行交叉编译的操作步骤，帮助用户更好地利用 Neuron 进行进一步的[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)业务开发。

Neuron 源码下载：

```
$ git clone https://github.com/emqx/neuron
$ cd neuron
$ git submodule update --init
$ mkdir build && cd build
```

## 什么是交叉编译

交叉编译，可以理解为在当前编译平台下，编译出能够运行在体系结构不同的另一种目标平台上的可执行程序的过程，经常用于目标平台无法运行编译所需的编译器的情况。

交叉编译需要用到交叉编译链。交叉编译链是为了编译跨平台体系结构的程序代码而形成的由多个子工具构成的一套完整的工具集。当指定了源文件（.c）时，它会自动按照编译流程调用不同的子工具，自动生成可执行文件。交叉编译链的重点在于交叉编译器，使用不同平台的编译器用来生成可在该平台运行的可执行程序。所有语句都写在跨平台编译工具 CMake 所依赖的规则文件 CMakeLists.txt 中，用于构建整个工程。

## Neuron 的交叉编译流程

下面我们以 X86_64 架构平台下编译出可运行于 armv7l 架构的可执行程序为例，介绍对 Neuron 源码进行交叉编译的具体操作。

### 安装编译器

执行以下指令安装适用于 armv7l 架构的编译器。

```
$ sudo apt-get update
$ sudo apt-get install -y gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf pkg-config libtool alien unzip
```

### 编写 .cmake 文件

.cmake 文件用于配置 cmake 的变量和属性。

```
# 目标系统名称
set(CMAKE_SYSTEM_NAME Linux)
set(COMPILER_PREFIX arm-linux-gnueabihf)
# 目标平台架构
set(CMAKE_SYSTEM_PROCESSOR armv7l)
# 库的目录
set(LIBRARY_DIR /opt/externs/libs)

# 语言编译器
set(CMAKE_C_COMPILER ${COMPILER_PREFIX}-gcc)
set(CMAKE_CXX_COMPILER ${COMPILER_PREFIX}-g++)

# 静态库的归档工具名称
set(CMAKE_AR ${COMPILER_PREFIX}-ar)
set(CMAKE_LINKER ${COMPILER_PREFIX}-ld)
set(CMAKE_NM ${COMPILER_PREFIX}-nm)
set(CMAKE_OBJDUMP ${COMPILER_PREFIX}-objdump)
# 静态库随机化工具名称
set(CMAKE_RANLIB ${COMPILER_PREFIX}-ranlib)
# CMAKE_STAGING_PREFIX 变量用于指定安装到主机的路经
set(CMAKE_STAGING_PREFIX ${LIBRARY_DIR}/${COMPILER_PREFIX})
# CMAKE_PREFIX_PATH 变量用于指定要编译的文件所在的安装位置
set(CMAKE_PREFIX_PATH ${CMAKE_STAGING_PREFIX})

include_directories(SYSTEM ${CMAKE_STAGING_PREFIX}/include)
include_directories(SYSTEM ${CMAKE_STAGING_PREFIX}/openssl/include)
# 指定交叉编译环境
set(CMAKE_FIND_ROOT_PATH ${CMAKE_STAGING_PREFIX})
# 从来不在指定目录下查找工具程序
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
# 只在指定目录下查找库文件
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
# 只在指定目录下查头文件
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
link_directories(${CMAKE_STAGING_PREFIX})
```

### 编写 CMakeLists.txt 文件

基础配置及参数配置如下：

```
# 设置 cmake 所需要的最低版本，如果用的 cmake 版本低于该版本，将报错
cmake_minimum_required(VERSION 3.12)
# 声明项目名称
project(neuron)
# 打开当前及其下级目录的测试功能
enable_testing()
# 打开 c 语言的支持
enable_language(C)
set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# build 类型，可取值 Debug，Release 等
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Debug")
endif()

# 要构建的目标平台的 CMake 标识符
if(NOT CMAKE_SYSTEM_NAME)
  set(CMAKE_SYSTEM_NAME "Linux")
endif()

if(CMAKE_SYSTEM_NAME MATCHES "Linux")
  add_definitions(-DNEU_PLATFORM_LINUX)
elseif(CMAKE_SYSTEM_NAME MATCHES "Darwin")
  add_definitions(-DNEU_PLATFORM_DARWIN)
elseif(CMAKE_SYSTEM_NAME MATCHES "Windows")
  add_definitions(-DNEU_PLATFORM_WINDOWS)
endif()

# 禁用告警：=ON 表示禁用，=OFF 表示不禁用
if(NOT DISABLE_WERROR)
  set(CMAKE_C_FLAGS "$ENV{CFLAGS} -Werror")
endif()

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -g")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS} -O1")

# 禁用内存错误检查：=ON 表示禁用，=OFF 表示不禁用
if(NOT DISABLE_ASAN)
  set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS} -fsanitize=address")
  set(CMAKE_CXX_FLAGS_DEBUG "-Wall -g -fsanitize=address")
endif()
```

依赖库的查找：

```
# 由 CMAKE_STAGING_PREFIX 参数选择依赖库文件查找的位置，该参数在 .cmake 文件中配置
if (CMAKE_STAGING_PREFIX)
  # 当进行交叉编译时，指定头文件的搜索路径
  include_directories(${CMAKE_STAGING_PREFIX}/include)
  # 添加需要链接的库文件目录
  link_directories(${CMAKE_STAGING_PREFIX}/lib)
else()
  # 当不进行交叉编译时，指定头文件的搜索路径
  include_directories(/usr/local/include)
  link_directories(/usr/local/lib)
endif()
```

指定 .c 源文件：

```
set(PERSIST_SOURCES
    src/persist/persist.c
    src/persist/json/persist_json_plugin.c)
set(NEURON_SOURCES
    src/main.c
    src/argparse.c
    src/daemon.c
    src/core/manager_internal.c
    src/core/manager.c
    src/core/subscribe.c
    src/core/sub_msg.c
    src/core/plugin_manager.c
    src/core/node_manager.c
    src/core/storage.c
    src/adapter/storage.c
    src/adapter/adapter.c
    src/adapter/driver/cache.c
    src/adapter/driver/driver.c
    plugins/restful/handle.c
    plugins/restful/license.c
    plugins/restful/license_handle.c
    plugins/restful/log_handle.c
    plugins/restful/normal_handle.c
    plugins/restful/rw_handle.c
    plugins/restful/adapter_handle.c
    plugins/restful/datatag_handle.c
    plugins/restful/group_config_handle.c
    plugins/restful/plugin_handle.c
    plugins/restful/version_handle.c
    plugins/restful/rest.c
    plugins/restful/http.c
    plugins/restful/proxy.c
    plugins/restful/websocket.c
    ${PERSIST_SOURCES})

# 设置 build 路径变量为当前路径
set(CMAKE_BUILD_RPATH ./)
# 定义可执行文件的名称为 neuron，编译可执行程序
add_executable(neuron)
# 指定源文件, 与 add_executable 合用，用于将源文件 NEURON_SOURCES 生成动态链接文件到 neuron 中。
target_sources(neuron PRIVATE ${NEURON_SOURCES}) 
# 将头文件库路径添加到 neuron 中
target_include_directories(neuron PRIVATE include/neuron src plugins)
# 将目标文件 neuron 与库文件进行链接
target_link_libraries(neuron dl neuron-base sqlite3 -lm)
```

### 依赖库的交叉编译

在源码交叉编译前，用户需要先对在交叉编译中使用的依赖库进行交叉编译，使得依赖库与交叉编译的平台保持一致。新建一个目录文件用于存放安装文件，例如 install。执行指令时所使用的编译工具，即上述中安装的相应的编译器。

cmake 通用参数说明

- -D 配置 cmake 的参数，功能类似于 set；

- CMAKE_C_COMPILER ，交叉编译宏变量，指定 c 的编译工具；
- CMAKE_CXX_COMPILER ，交叉编译宏变量，指定 c++ 的编译工具 ；
- CMAKE_STAGING_PREFIX ，交叉编译变量，指定安装到主机上的路径 ；
- CMAKE_PREFIX_PATH，交叉编译变量，指定要编译的文件所在的安装位置；

#### [zlog](https://github.com/HardySimpson/zlog.git)

在 install 目录下，执行以下指令安装 zlog 依赖库。

```
$ git clone -b 1.2.15 https://github.com/HardySimpson/zlog.git
$ cd zlog     
$ make CC=arm-linux-gnueabihf-gcc
$ sudo make PREFIX=/opt/externs/libs/arm-linux-gnueabihf install
```

#### [jansson](https://github.com/neugates/jansson.git)

在 install 目录下，执行以下指令安装 jansson 依赖库。

```
$ git clone https://github.com/neugates/jansson.git
$ mkdir build && cd build
$ cmake .. -DCMAKE_C_COMPILER=arm-linux-gnueabihf-gcc -DCMAKE_CXX_COMPILER=arm-linux-gnueabihf-g++ -DCMAKE_STAGING_PREFIX=/opt/externs/libs/arm-linux-gnueabihf -DCMAKE_PREFIX_PATH=/opt/externs/libs/arm-linux-gnueabihf -DJANSSON_BUILD_DOCS=OFF -DJANSSON_EXAMPLES=OFF
$ make
$ sudo make install     
```

#### [mbedtls](https://github.com/Mbed-TLS/mbedtls.git)

在 install 目录下，执行以下指令安装 mbedtls 依赖库。

```
$ git clone -b v2.16.12 https://github.com/Mbed-TLS/mbedtls.git
$ cd mbedtls && mkdir build && cd build
$ cmake -DCMAKE_C_COMPILER=arm-linux-gnueabihf-gcc -DCMAKE_CXX_COMPILER=arm-linux-gnueabihf-g++ -DUSE_SHARED_MBEDTLS_LIBRARY=OFF -DENABLE_TESTING=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON .. && make && sudo make install
```

#### [jwt](https://github.com/benmcollins/libjwt.git)

在 install 目录下，执行以下指令安装 jwt 依赖库。

```
$ git clone https://github.com/benmcollins/libjwt.git
$ cd libjwt
$ mkdir build && cd build
$ cmake .. -DCMAKE_C_COMPILER=arm-linux-gnueabihf-gcc -DCMAKE_CXX_COMPILER=arm-linux-gnueabihf-g++ -DCMAKE_STAGING_PREFIX=/opt/externs/libs/arm-linux-gnueabihf -DCMAKE_PREFIX_PATH=/opt/externs/libs/arm-linux-gnueabihf -DENABLE_PIC=ON -DBUILD_SHARED_LIBS=OFF
$ make
$ sudo make install
```

#### [NanoSDK](https://github.com/neugates/NanoSDK.git)

```
$ git clone -b neuron https://github.com/neugates/NanoSDK.git
$ cd NanoSDK && mkdir build && cd build
$ cmake -DBUILD_SHARED_LIBS=OFF -DNNG_TESTS=OFF -DNNG_ENABLE_SQLITE=ON -DNNG_ENABLE_TLS=ON .. && make && sudo make install
```

#### [sqlite3](https://github.com/sqlite/sqlite)

在 install 目录下，执行以下指令安装 sqlite3 依赖库。

```
$ curl https://www.sqlite.org/2022/sqlite-autoconf-3390000.tar.gz --output sqlite3.tar.gz
$ mkdir -p sqlite3
$ tar xzf sqlite3.tar.gz --strip-components=1 -C sqlite3
$ cd sqlite3
$ ./configure --prefix=/opt/externs/libs/arm-linux-gnueabihf --disable-shared --disable-readline --host armv4 CC=arm-linux-gnueabihf-gcc
$ make
$ sudo make install     
```

依赖库编译可参考 https://github.com/emqx/neuron/blob/main/Install-dependencies.md 。

### Neuron 源码交叉编译

完成以上步骤后，执行以下指令下编译 Neuron 源码，生成目标平台可执行文件。

```
$ cmake .. -DCMAKE_TOOLCHAIN_FILE=../cmake/arm-linux-gnueabihf.cmake -DCMAKE_BUILD_TYPE=Release -DDISABLE_UT=ON
$ make
```

DISABLE_UT 参数，禁用单元测试，=ON 禁用，=OFF 不禁用。

CMAKE_TOOLCHAIN_FILE 参数用于指定 .cmake 文件的路径。

## 结语

至此，我们就完成了使用 Neuron 源码进行交叉编译的全部操作。用户可以根据本文，自行编译出所需架构的可执行文件，从而更好地将 Neuron 运行在不同架构平台上，实现相应的业务目标。

有关 Neuron 开源版使用中的任何建议或问题，欢迎在 GitHub 仓库提交 PR 和 Issues：[https://github.com/emqx/neuron](https://github.com/emqx/neuron)




<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
