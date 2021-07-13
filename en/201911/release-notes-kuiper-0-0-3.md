Date: 2019/11/20

The Kuiper team would like to announce the release of Kuiper 0.0.3

Kuiper 0.0.3 is [available for download](https://github.com/emqx/kuiper/releases/tag/0.0.3).

Kuiper is a SQL based lightweight IoT analytics/streaming software running at resource constrained edge devices. This release includes several new features and bug fixes.

Website: https://github.com/lf-edge/ekuiper

Github Repository: https://github.com/emqx/kuiper

## Overview 

### Features

- Refactor the code to support Kuiper Sink and Source extension.
- Enhanced MQTT Sink to support AWS IoT and Azure IoT Hub. User can directly publish result to any MQTT IoT Hub by configuring Sink.
- Enhanced MQTT Source to support secured settings. User can specifiy username, password, certifications and private key information for MQTT source.
- HAVING clause support
- Added Chinese document, and renamed XStream to Kuiper in all of documents.
- Build improvement
  - Added build version number in command line tools
  - Updated Makefile, and now supports automatically build for all platforms

### Bug fixes

- [#7](https://github.com/emqx/kuiper/issues/7) GROUP BY issue
- [#13](https://github.com/emqx/kuiper/issues/13) Kuiper server quits when a rule is drop

### Contact

If having any problems for Kuiper, feel free to contact us through contact@emqx.io



------

Welcome to our open source project [github.com/emqx/emqx](https://github.com/emqx/emqx). Please visit the [ documentation](https://docs.emqx.io) for details.

