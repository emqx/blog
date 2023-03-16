In January, the eKuiper team launched [v1.8.0](https://www.emqx.com/en/blog/ekuiper-v-1-8-0-release-notes) and refined the accompanying documentation in February.

Development work on v1.9.0, has already begun, which aims to facilitate the connection of the industrial protocol gateway Neuron with multiple instances. The team has already completed feature research, planning, and the creation of a new Python virtual environment.

Additionally, v1.8.1 has been released this month, featuring the Portable plugin import and bug fixes for the Flow Editor. Further information can be found at [https://github.com/lf-edge/ekuiper/releases/tag/1.8.1](https://github.com/lf-edge/ekuiper/releases/tag/1.8.1).

## Support Python Virtual Environment

Python developers often use virtual environments to manage dependencies. The most popular Python environment manager is Anaconda or Miniconda, both of which include the [conda](https://conda.io/projects/conda/en/latest/index.html) package and environment manager in all versions. eKuiper allows the running of Python plugins using the conda environment.

However, before using this feature, you must ensure that the host or Docker container running eKuiper has a conda virtual environment configured for Python. The process of using this feature is similar to that of a regular Python plugin, except for specifying the name of the virtual environment to be used when creating the JSON metafile during the plugin packaging phase. An example of this is shown below.

```
{
  "version": "v1.0.0",
  "language": "python",
  "executable": "pysam.py",
  "virtualEnvType": "conda",
  "env": "myenv",
  "sources": [
    "pyjson"
  ],
  "sinks": [
    "print"
  ],
  "functions": [
    "revert"
  ]
}
```

In the above example, the virtual environment type is specified as conda, and the name of the virtual environment is specified as myenv so that the plugin can run in the conda's myenv environment. Presently, only conda is supported.

## Coming Soon

Our primary focus next month will be developing the additional features of v1.9.0, which we expect to release alongside Neuron towards the end of the following month or shortly after that. In this version, we will modify the connection process to Neuron to facilitate multi-instance connections. Additionally, we will be working on other features, including local configuration bulk distribution to streamline multi-instance configuration management, and dynamic token support for HTTP Pull Source, providing support for a wider range of HTTP data sources. We are thrilled to unveil these new updates, so stay tuned for more information!
