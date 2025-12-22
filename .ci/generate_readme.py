import copy
import os
import sys

import requests

base_path = sys.argv[1]

if __name__ == '__main__':
    langs = ['en', 'ja', 'zh']
    category_dict = {
        # Main categories
        'product': {'label': 'Product', 'description': 'EMQ products including EMQX, EMQX Cloud, Neuron, NanoMQ, MQTTX and more.', 'sub': ['emqx', 'cloud', 'enterprise', 'neuron', 'nanomq', 'mqttx', 'kuiper', 'xmeter', 'releases', 'newsletter']},
        'mqtt': {'label': 'MQTT', 'description': 'Learn MQTT protocol from beginner to advanced, including tutorials, clients, programming and security.', 'sub': ['mqtt client', 'mqtt protocol', 'mqtt programming', 'mqtt broker', 'security', 'iot testing']},
        'integration': {'label': 'Integration', 'description': 'Integrate MQTT with databases, message queues, cloud services and more.', 'sub': ['eco and integration']},
        'use cases': {'label': 'Use Cases', 'description': 'Real-world IoT solutions and industry applications powered by EMQ.', 'sub': ['use cases', 'solutions']},
        'ai': {'label': 'AI', 'description': 'Empower IoT with AI and LLM capabilities.', 'sub': ['ai']},
        'iov': {'label': 'Internet of Vehicles', 'description': 'Build reliable and efficient connected vehicle platforms with EMQ.', 'sub': ['internet of vehicles']},
        'iiot': {'label': 'Industrial IoT', 'description': 'Industrial IoT solutions with Unified Namespace and Sparkplug.', 'sub': ['industrial iot']},
        # Standalone categories
        'engineering': {'label': 'Engineering', 'description': 'Technical deep dives and engineering insights.'},
        'community': {'label': 'Community', 'description': 'Community news, events and contributions.'},
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

        api = f'https://www.emqx.com/api/v1/blog?_sort=createAt&_limit=1000'
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
            file_path = f'https://github.com/emqx/blog/edit/main/{lang}/{blog_date}/{blog_title_url}.md'
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
