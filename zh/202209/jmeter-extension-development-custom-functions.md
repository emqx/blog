强大的扩展性是压力测试工具 JMeter 的一个重要特点。虽然本身内置的函数、协议支持有限，但是 JMeter 提供了良好的扩展框架，允许使用者对其进行扩展。

本文将介绍如何利用 JMeter 的扩展性来实现自定义的函数，用户可以通过此方式扩展出性能测试过程中所需要的函数功能。

## JMeter 函数简介

由于 JMeter 函数相对简单，本文便以它作为起点。

JMeter 函数（function）可以让用户在编辑测试脚本的时候插入到任何 Sampler 或者其他测试元素中，执行相应的任务。比如，`__machineName` 取得 JMeter Agent 所在机器的主机名，`__machineIP` 取得 JMeter Agent 所在机器的 IP 地址，`__RandomString` 得到一个随机的字符串。JMeter 所提供的内置函数完整列表，请参考[官方文档](http://jmeter.apache.org/usermanual/functions.html)。

总体来说，扩展 JMeter 的函数可以分成下面几个步骤：

1. 在 IDE （以下将以 Eclipse 为例）中新建 Maven 项目，引入扩展 JMeter 函数所需的依赖；
2. 编写实现自定义函数的代码，并对其编译打包；
3. 将编译好的包拷贝至 JMeter 的扩展目录，编辑测试脚本，在脚本中使用自定义的函数；
4. 运行自定义的函数，查看运行结果是否正确。

接下来我们将以一个返回随机偶数的自定义函数为例，来带大家了解完整的开发过程。



## 创建扩展 JMeter 项目

本例中将使用 Maven 来管理依赖并进行打包。

在 Eclipse 中新建一个 Maven 项目：File > New > Project，选择 Maven Project，如下图所示：

![在 Eclipse 中新建一个 Maven 项目](https://assets.emqx.com/images/84ebcef8269df5eaf062aabe64a86855.png)

在向导的第 2 页里，选择 Create a simple project (skip archetype selection)，使用默认的 Workspace，或指定 Workspace 位置，并点击下一步：

![New Maven Project 2](https://assets.emqx.com/images/22a12fdc087b681e0b99fef05e29ed77.png)

在向导的第 3 页，指定 Group Id 和 Artifact Id。点击完成，完成项目的创建：

![New Maven Project 3](https://assets.emqx.com/images/b51510d94928a4accebe8b27836d5cb6.png)

## 通过 Maven 引入相应的 JMeter 依赖

打开 pom.xml ，在 <dependencies> 中加入 JMeter 的 ApacheJMeter_core 和 ApacheJMeter_functions 依赖，如下所示：

```
 <dependencies>
    <dependency>
        <groupId>org.apache.jmeter</groupId>
        <artifactId>ApacheJMeter_core</artifactId>
        <version>5.4.3</version>
        <scope>provided</scope>
    </dependency>
    <dependency>
        <groupId>org.apache.jmeter</groupId>
        <artifactId>ApacheJMeter_functions</artifactId>
        <version>5.4.3</version>
        <scope>provided</scope>
    </dependency>
 </dependencies>
```

由于 ApacheJMeter_core 和 ApacheJMeter_functions 已经包含在 JMeter 的运行时中，所以后面编译打包出来的 jar 不需要包含它们，此处将这两个依赖的 scope 设为 provided。

保存 pom.xml 后，如果 Maven 没有开始自动下载相关的依赖文件，在项目上右键点击，选择 Maven > Update Project，完成依赖的下载。

## 扩展 JMeter 函数

要实现扩展 JMeter 函数，有两处要点：

1. 实现函数功能的类所在的 package 的声明必须包含".functions"
2. 实现类继承 org.apache.jmeter.functions.AbstractFunction，并且编写相应方法的实现逻辑。

#### package 名字

JMeter 可以通过非 UI 方式运行，因为它的设计中让一些核心的类（非 UI 相关的，比如 ApacheJMeter_core 等）可以在非 UI 运行方式下被优先加载进来，加载这些类的时候是通过命名规则来实现的。所有实现 JMeter 函数的类必须包含".functions."，因此我们自定义实现的类里也必须遵守这一规则，比如，类所在的 package 名称为"com.xmeter.customized.functions"。当然也可以通过更改 jmeter.properties 中的配置来实现改变命名规则，如下图所示（但一般来说不推荐更改此项配置）：

```
classfinder.functions.contain=.functions.
```

#### 扩展 AbstractFunction 类

ApacheJMeter_core 中的 AbstractFunction 类提供了4个抽象方法，在扩展的时候需要实现它们。

方法 1：

```
public String execute(SampleResult previousResult, Sampler currentSampler) throws InvalidVariableException;
```

JMeter 会将上次运行的 SampleResult 和当前的 Sampler 作为参数传入 execute 方法中，方法的返回值就是在运行该函数后应得到的值，返回类型为 String 类型。该方法如果操作了非线程安全的对象（比如文件），则需要对该方法进行线程同步保护。

方法 2：

```
public List<String> getArgumentDesc();
```

getArgumentDesc 方法用于告诉 JMeter 关于你实现的函数所需的参数的描述。

方法 3：

```
public void setParameters(Collection<CompoundVariable> parameters) throws InvalidVariableException;
```

setParameters 方法用于传递用户在执行过程中传入的函数所需的实际参数值。该方法在函数没有参数的情况下也会被调用。一般该方法传入的参数会被保存在实现类中的全局变量里，并在其后 JMeter 调用到 execute 方法时使用到。

方法 4：

```
public String getReferenceKey();
```

getReferenceKey 方法返回的就是此处自定义的函数的名字。JMeter 约定的命名规则是在函数名前面加入双下划线"__"。建议函数的名字跟实现类的类名保持一致，而且 getReferenceKey 方法返回的名字以 static final 的方式在实现类中定义好，避免在运行的时候更改它。

#### 源代码实现

实现的源代码如下所示，重要的代码已经有注释。

```
package com.emqx.xmeter.demo.functions;

import java.util.Collection;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;

import org.apache.jmeter.engine.util.CompoundVariable;
import org.apache.jmeter.functions.AbstractFunction;
import org.apache.jmeter.functions.InvalidVariableException;
import org.apache.jmeter.samplers.SampleResult;
import org.apache.jmeter.samplers.Sampler;

public class MyRandomFunc extends AbstractFunction {

    //自定义function的描述
    private static final List<String> desc = new LinkedList<String>();
    static {
        desc.add("Get a random int within specified parameter value.");
    }

    //function名称
    private static final String KEY = "__MyRandomFunc";

    private static final int MAX_PARA_COUNT = 1;
    private static final int MIN_PARA_COUNT = 1;

    //传入参数的值
    private Object[] values;

    private Random r = new Random();

    @Override
    public List<String> getArgumentDesc() {
        return desc;
    }

    @Override
    public String execute(SampleResult previousResult, Sampler currentSampler) throws InvalidVariableException {
        try {
            int max = new Integer(((CompoundVariable) values[0]).execute().trim());
            int val = r.nextInt(max);
            return String.valueOf(val);
        } catch(Exception ex) {
            throw new InvalidVariableException(ex);
        }
    }

    @Override
    public String getReferenceKey() {
        return KEY;
    }

    @Override
    public void setParameters(Collection<CompoundVariable> parameters) throws InvalidVariableException {
         checkParameterCount(parameters, MIN_PARA_COUNT, MAX_PARA_COUNT); //检查参数的个数是否正确
         values = parameters.toArray(); //将值存入类变量中
    }

}
```

## 编译并拷贝到 JMeter 扩展目录

接下来的一步就是要把实现类编译生成 jar 包并且拷贝到 JMeter 的扩展目录。编译打包部分可参考以下的 Maven <build>：

```
<build>
  <finalName>my-demo-plugins-${project.version}</finalName>
	<plugins>
		<plugin>
			<groupId>org.apache.maven.plugins</groupId>
			<artifactId>maven-compiler-plugin</artifactId>
			<version>3.8.0</version>
			<configuration>
				<source>1.8</source>
				<target>1.8</target>
			</configuration>
		</plugin>
		<plugin>
			<groupId>org.apache.maven.plugins</groupId>
			<artifactId>maven-assembly-plugin</artifactId>
			<configuration>
				<!-- 打包方式 -->
				<descriptorRefs>
					<descriptorRef>jar-with-dependencies</descriptorRef>
				</descriptorRefs>
			</configuration>
			<executions>
				<execution>
					<id>assemble-all</id>
					<phase>package</phase><!-- 绑定到package阶段上 -->
					<goals>
						<goal>single</goal>
					</goals>
				</execution>
			</executions>
		</plugin>
	</plugins>
</build>
```

接下来在 Eclipse 中新增一个 Maven Build 的运行配置，请参见下图：

![Maven Build 的运行配置](https://assets.emqx.com/images/1c3f21e43c7b0a4dbe236dc80913a356.png)

运行上面这个 Maven Build 之后，在工程的 target 目录下，会发现新生成了 my-demo-plugins-0.0.1-SNAPSHOT-jar-with-dependencies.jar。把这个jar 拷贝至 $JMETER_HOME/lib/ext 目录下（$JMETER_HOME 指 JMeter 的安装目录），重新启动 JMeter。

点击工具 > 函数助手对话框，如果配置正确的话就能出现自己定义的函数，如下图所示。点击右下角的"生成"按钮，会生成调用该函数后生成的示例结果。

![JMeter 函数助手](https://assets.emqx.com/images/963454f15790eed2b1395e164b677275.png)

## 测试自定义函数

最后我们创建一个测试，来验证该 JMeter 函数工作是否正常，我们将使用 Dummy Sampler 作为测试用的取样器。Dummy Sampler 是一个第三方扩展的取样器，提供基本的请求和响应模拟功能，在脚本调试或 JMeter 学习期间可以作为简单的模拟数据生成器来使用。Dummy Sampler 在 JMeter 社区中可以找到，我们先介绍一下它的安装方法。

Dummy Sampler 可以通过 JMeter 插件管理器完成安装。

1. 打开页面 [插件管理网站](https://jmeter-plugins.org/install/Install/)，搜索并下载 plugins-manager，或直接点击以下链接下载：https://jmeter-plugins.org/get/
2. 将下载的 jmeter-plugins-manager-1.7 放到 $JMETER_HOME/lib/ext 目录下，并重启 JMeter。
3. 如果安装成功，重启 JMeter 后，菜单"选项"中将出现"Plugins Manager"：
   ![点击 Plugins Manager](https://assets.emqx.com/images/a683895f3b031652d61acf081ff7aab9.png)
4. 打开"Plugins Manager"后，选择"Available Plugins"，在左侧的列表中搜索并选择"Dummy Sampler"，然后点击"Apply Changes and Restart JMeter"按钮。如下图所示：
   ![选择"Available Plugins"](https://assets.emqx.com/images/0d3a9d7152490432fc26df0999bf786a.png)
5. JMeter的Plugins Manager 将下载相关文件，并且在安装完成后自动重启 JMeter。打开"Plugins Manager"后，将发现"Dummy Sampler"已出现在"Installed Plugins"中。

接下来，我们在测试脚本中使用 Dummy Sampler。先在线程组中添加 > 取样器 > jp@gc - Dummy Sampler：

![使用 Dummy Sampler](https://assets.emqx.com/images/5dd9c0add395f9af24f024bc0f0d5beb.png)

可以进一步设置请求内容、连接时间、延迟时间、响应时间、响应码、响应内容等模拟数据。在这次测试中，我们将自定义函数生成的随机数设置为响应内容，参数设为 100，也就是指定生成小于 100 的偶数。

![JMeter 设置 Dummy Sampler](https://assets.emqx.com/images/c322d8d821bf8f8e2e2946583ba5251d.png)

为方便查看测试结果，添加监听器，如"察看结果树"。然后运行测试，如果一切正常，在"响应数据"部分应该就能看到由该函数生成的随机整数了。

![JMeter 察看结果树](https://assets.emqx.com/images/f4f0a4e32fff2eb9165e2fb18f5e398a.png)


<section class="promotion">
    <div>
        免费试用 XMeter Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 负载测试云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https%3A%2F%2Fxmeter-cloud.emqx.com%2FcommercialPage.html" class="button is-gradient px-5">开始试用 →</a>
</section>


## 参考文献

[http://www.javacodegeeks.com/2013/06/jmeter-custom-function-implementation.html](https://link.jianshu.com/?t=http://www.javacodegeeks.com/2013/06/jmeter-custom-function-implementation.html)

[http://jmeter.apache.org/usermanual/functions.html](http://jmeter.apache.org/usermanual/functions.html)
