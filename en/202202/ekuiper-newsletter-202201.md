The milestone version 1.4.0 of eKuiper has been officially released, and many friends have already started to use it. In particular, some new features that complement the shortcomings have been highly praised by the community, such as python plugins, rule pipelines, dynamic parameters, etc.

In January, we have successively released two minor versions to continuously fix the problems reported by users and improve product stability and user experience. At the same time, in the first month of the new year, the eKuiper team also started the development of the next milestone version v1.5.0. We have completed some functions and merged them into the development branch, which is convenient for the early adopter of the community.

## v1.4.1 and v1.4.2 arrived one after another with continuous improvement

Versions 1.4.1 and 1.4.2 released this month are dedicated to improving product stability and optimizing product performance and documentation. It is recommended that users upgrade directly to v1.4.2 for a better experience. The main improvements in these two versions are as follows:

### Optimizations of the support for Portable plugin

The target system using the Python plugin needs to install the python 3.x environment and the dependent eKuiper plugin runtime. In the case of container deployment, users need to install and configure the environment in the official Docker image, which is inconvenient. In the new version, the image of python environment with eKuiper and plugin is officially provided. Users can use the python plugin out of the box. Please use the image with the suffix of `-slim-python`, such as `lfedge/ekuiper:1.4. 2-slim-python`. At the same time, in dockerhub, we provide a tag of the major version number, which will automatically obtain the latest minor version of the image under the major version. For example, `lfedge/ekuiper:1.4-alpine` will automatically point to the image of the latest 1.4.x version. Currently, it will point to the image of 1.4.2 version.

In terms of plugin runtime, we also fixed issues related to stability and performance, and updated some plugin examples. Previously, when the plugin SDK runs a custom function (except source and sink), the connection with the main program will be out of order. Users need to update the corresponding plugin SDK version to solve this problem. In addition, the new function plugin caches the result of the isAggregate function at runtime to avoid the need to query every time, so as to improve performance.

### Modification of dynamic parameters of Sink

The JSONPath syntax starting with the `$` was previously supported in the dynamic parameters. However, for some users, their MQTT Topic itself starts with `$`, which results in conflicts and causes this type of Topic unable to work properly. In Sink, the syntax of data template is used to format the output results, which is powerful, flexible and widely used. In the new version, the dynamic parameters adopt the same syntax as the data template, so that users can output results more flexibly without learning new syntax. For text formatting, data template syntax is more flexible than JSONPath syntax and supports more formatting functions. In the following example, it sends the result to a dynamic MQTT topic for the rule. Thanks to the syntax of the data template, the topic can be easily prefixed, suffixed or formatted in a more complex way.

```
{
  "id": "rule1",
  "sql": "SELECT topic FROM demo",
  "actions": [{
    "mqtt": {
      "sendSingle": true,
      "topic": "prefix/{{.topic}}"
    }
  }]
}
```

Users who originally used JSONPath syntax in MQTT Sink are recommended to modify it to a new format. If you still need to use the old syntax, you can change the prefix to `($` to distinguish it from common MQTT topics.

### Edgex object type support

A new data type Object was added in the EdgeX Foundry Jarkata, which can be used to store complex structured data, such as maps. In the new version, both EdgeX source and Sink of eKuiper are adapted to this type and can be parsed normally without additional configuration. For reading into the EdgeX object type of eKuiper, you can directly use eKuiper's json syntax to read, operate, convert, etc. For example, if you read the Resource named `obj` whose Object value is `{"a":"string","b",1}`, you can access the nested value through `obj->a` in eKuiper SQL. At the same time, the map type in the output of eKuiepr will be automatically set to the object type when it is sent to EdgeX.

### Other improvements

- Improve UI adaptation: Solve multiple UI problems, such as shared connection configuration, plugin installation page error, display problems of Chinese name rules, etc.
- Runtime performance optimization. In the test case of shared source multiple rules, the CPU usage is reduced by another 20% based on the previous version.
- HTTP source and sink support configuring https certificates.
- For other bug fixes, see [1.4.1](https://github.com/lf-edge/ekuiper/releases/tag/1.4.1) and [1.4.2](https://github.com/lf-edge/ekuiper/releases/tag/1.4.2) release notes.

## Start 1.5.0 development

The next milestone version v1.5.0 has entered the development stage. The main feature done so far is to compile on demand.

### Compile on demand

As an edge streaming engine, there are many heterogeneous target systems to be deployed, including edge computer rooms and gateways with better computing power, as well as cheaper or customized software and hardware solutions for the consideration of cost and special business requirements. With the gradual enhancement of functions, the full-featured eKuiper may be slightly heavy on devices with extreme resource constraints, such as terminals with less than 50MB of memory. In the new version, we strip the core functions and other functions of eKuiper through the compiled tags of the go language. When users use it, they can compile some functions on demand by setting the compilation parameters, so as to obtain a smaller running file. For example, you can use `make build_core` to get a run file containing only core functionality. For further information, please refer to [compile on demand](https://github.com/lf-edge/ekuiper/blob/1.5.0/docs/zh_CN/features.md).

## Documentation update

According to user feedback, we will continue to improve the documentation and add more examples and cases in the new year. We have already adjusted the structure of the documentation, reducing the main directory tree of the documentation into installation, user guide, rules, SQL and extensions, so as to facilitate users to find the required information. You can click [eKuiper Documentation](https://ekuiper.org/docs/en/latest/) to view it and submit feedback.
