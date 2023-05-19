import os
import sys

import requests

base_path = sys.argv[1]

if __name__ == '__main__':
    langs = ['en']
    category_sort = ['emqx', 'cloud', 'enterprise', 'neuron', 'mqtt protocol', 'mqtt broker', 
              'mqtt client', 'mqtt programming', 'security', 'internet of vehicles', 
              'industrial iot', 'eco and integration', 'iot testing', 'nanomq', 
              'mqttx', 'kuiper', 'xmeter']
    for lang in langs:
        if lang == 'en':
            readme_path = os.path.join(base_path, 'README.md')
        api = f'https://www.emqx.com/api/v1/blog?_sort=createAt&_limit=1000&site=com'
        blog_records = requests.get(url=api, headers={'Content-Language': lang}).json()
        if not blog_records['success']:
            print(f'Failed to get blog records: {blog_records}')
            exit(1)
        readme_content = f'# EMQX Blog\n\n'
        category_options = blog_records['data']['categoryOption']
        category_records = {category_option['value']: {'category_label': category_option['label'], 'category_url': f'https://www.emqx.com/{lang}/blog/category/{category_option["value"].replace(" ", "-")}', 'blogs': []} for category_option in category_options}
        blog_records = blog_records['data']['items']
        for blog_record in blog_records:
            blog_lang = blog_record['language']
            blog_title = blog_record['title']
            blog_categories = blog_record['category']
            if blog_lang != lang:
                continue
            blog_date = '' .join(blog_record['createAt'].split('-')[:2]).replace('-', '')
            blog_title_url = blog_record['titleUrl']
            file_path = f'https://github.com/emqx/blog/blob/main/{lang}/{blog_date}/{blog_title_url}.md'
            for c in blog_categories:
                category_records[c]['blogs'].append({'title': blog_title, 'path': file_path})
        category_records = {k: v for k, v in sorted(category_records.items(), key=lambda item: category_sort.index(item[0]) if item[0] in category_sort else len(category_sort))}
        for category, category_records in category_records.items():
            if len(category_records['blogs']) == 0:
                continue
            readme_content += f'\n\n## [{category_records["category_label"]}]({category_records["category_url"]})\n\n'
            for record in category_records['blogs']:
                readme_content += f'- [{record["title"]}]({record["path"]})\n'
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
