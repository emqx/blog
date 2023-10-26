import copy
import os
import sys

import requests

base_path = sys.argv[1]

if __name__ == '__main__':
    langs = ['en', 'ja', 'zh']
    category_dict = {
        'mqtt protocol': {'label': 'MQTT Tutorials', 'description': 'Get to know the preferred protocol in IoT from beginner to master.'},
        'mqtt broker': {'label': 'MQTT Broker', 'description': ''},
        'mqtt client': {'label': 'MQTT Client', 'description': ''},
        'mqtt programming': {'label': 'MQTT Programming', 'description': 'Best practice of MQTT in various clients.'},
        'security': {'label': 'MQTT Security', 'description': ''},
        'eco and integration': {'label': 'MQTT Integration (Eco & Integration)', 'description': 'Explore more with & via EMQ.'},
        'emqx': {'label': 'EMQX Open Source | Broker', 'description': 'EMQX is the world\'s most scalable open-source MQTT broker with a high performance that connects 100M+ IoT devices in 1 cluster, while maintaining 1M message per second throughput and sub-millisecond latency.'},
        'cloud': {'label': 'EMQX Cloud', 'description': 'The easiest way to start MQTT service. Connect your IoT devices to any cloud without the burden of maintaining infrastructure.'},
        'enterprise': {'label': 'EMQX Enterprise', 'description': 'The world\'s most scalable and reliable MQTT messaging platform to connect, move and process your data in business-critical scenarios for the IoT era.'},
        'internet of vehicles': {'label': 'Internet of Vehicles | Connected Cars', 'description': 'Build a reliable, efficient and industry-specific Internet of Vehicles platform based on EMQ\'s practical experience, from theoretical knowledge such as protocol selection to practical operations like platform architecture design.'},
        'industrial iot': {'label': 'Industrial IoT | Unified Namespace | Sparkplug', 'description': ''},
        'mqttx': {'label': 'MQTTX', 'description': 'MQTTX is a Fully Open-source MQTT 5.0 cross-platform Desktop Client, makes it easy and quick to create multiple simultaneous online MQTT client connections, test the connection, publish, and subscribe functions of MQTT/TCP, MQTT/TLS, MQTT/WebSocket as well as other MQTT protocol features.'},
        'neuron': {'label': 'Neuron - IIoT Connectivity Server', 'description': 'IoT edge industrial protocol gateway software, which supports one-stop access to dozens of industrial protocols and converts them into MQTT protocol to access the cloud industrial IoT platform. It just requires ultra-low resource consumption, and supports three major architectures of X86, ARM, and MIPS.'},
        'nanomq': {'label': 'NanoMQ - Lightweight MQTT broker for IoT Edge', 'description': 'NanoMQ is an MQTT messaging broker + multi-protocol message bus for edge computing. It supports the MQTT protocol and other commonly-used edge bus protocols such as ZeroMQ and Nanomsg, and integrates broker and brokerless message modes to facilitate the creation of one-stop edge data bus applications.'},
        'kuiper': {'label': 'eKuiper', 'description': 'eKuiper is an edge lightweight IoT data analytics / streaming software implemented by Golang, and it can be run at all kinds of resource constrained edge devices.'},
        'xmeter': {'label': 'XMeter', 'description': 'XMeter support millions of simulated users, concurrent device connections, and message throughput performance testing. XMeter support the testing of many IoT protocols such as MQTT, LwM2M/CoAP, and can extend richer test scenarios and protocol support for IoT applications.'},
        'solutions': {'label': 'Solutions', 'description': 'Accelerate digital transformation of industries based on EMQ data infrastructure for IoT.'},
        'engineering': {'label': 'Engineering', 'description': ''},
        'community': {'label': 'Community', 'description': ''},
        'iot testing': {'label': 'IoT Testing', 'description': 'Guarantee the availability and reliability of the IoT platform.'},
    }

    for lang in langs:
        category_sort = copy.deepcopy(category_dict)
        for k, v in category_sort.items():
            category_sort[k]['url'] = f'https://www.emqx.com/{lang}/blog/category/{k.replace(" ", "-")}'
            category_sort[k]['sort'] = list(category_sort.keys()).index(k)
        if lang == 'en':
            readme_path = os.path.join(base_path, 'README.md')
        else:
            readme_path = os.path.join(base_path, f'README-{lang.upper()}.md')

        api = f'https://www.emqx.com/api/v1/blog?_sort=createAt&_limit=1000&site=com'
        blog_records = requests.get(url=api, headers={'Content-Language': lang}).json()
        if not blog_records['success']:
            print(f'Failed to get blog records: {blog_records}')
            exit(1)
        readme_content = f'# EMQX Blog\n\n'
        readme_content += '[English](./README.md) | [简体中文](./README-ZH.md) | [日本語](./README-JA.md)\n\n'

        category_options = blog_records['data']['categoryOption']
        category_index = len(category_sort.keys())
        for category_option in category_options:
            if category_option['value'] not in category_sort:
                category_sort[category_option['value']] = {'label': category_option['label'], 'description': '', 'url': f'https://www.emqx.com/{lang}/blog/category/{category_option["value"].replace(" ", "-")}', 'sort': category_index + 1}

        blog_records = blog_records['data']['items']
        for blog_record in blog_records:
            blog_lang = blog_record['language']
            blog_title = blog_record['title']
            blog_categories = blog_record['category']
            if blog_lang != lang:
                continue
            blog_date = '' .join(blog_record['createAt'].split('-')[:2]).replace('-', '')
            blog_title_url = blog_record['titleUrl']
            blog_url = f'https://www.emqx.com/{lang}/blog/{blog_title_url}'
            file_path = f'https://github.com/emqx/blog/blob/main/{lang}/{blog_date}/{blog_title_url}.md'
            for c in blog_categories:
                if 'blogs' not in category_sort[c]:
                    category_sort[c]['blogs'] = []
                category_sort[c]['blogs'].append({'title': blog_title, 'path': file_path, 'url': blog_url})

        category_sort = dict(sorted(category_sort.items(), key=lambda x: x[1]['sort']))
        for category, category_records in category_sort.items():
            if len(category_records.get('blogs', [])) == 0:
                continue
            readme_content += f'\n\n## [{category_records["label"]}]({category_records["url"]})'
            if category_records['description']:
                readme_content += f'\n{category_records["description"]}\n\n'
            else:
                readme_content += '\n\n'
            for record in category_records['blogs']:
                readme_content += f'- [{record["title"]}]({record["url"]})'
                readme_content += f' ([Edit]({record["path"]}))\n'

        with open(readme_path, 'w') as f:
            f.write(readme_content)
