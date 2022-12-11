import os
import sys

import requests

base_path = sys.argv[1]

if __name__ == '__main__':
    langs = ['zh', 'en', 'id']
    for site in ['com', 'hstream']:
        for lang in langs:
            api = f'https://www.emqx.com/api/v1/blog?_sort=updateAt&_limit=50&site={site}'
            blog_records = requests.get(url=api, headers={'Content-Language': lang}).json()
            if not blog_records['success']:
                print(f'Failed to get blog records: {blog_records}')
                exit(1)
            blog_records = blog_records['data']['items']
            for blog_record in blog_records:
                blog_lang = blog_record['language']
                blog_date = '' .join(blog_record['createAt'].split('-')[:2]).replace('-', '')
                blog_title_url = blog_record['titleUrl']
                blog_content = blog_record['contents']
                if not os.path.exists(os.path.join(base_path, blog_lang, blog_date)):
                    os.makedirs(os.path.join(base_path, blog_lang, blog_date))

                f = open(os.path.join(base_path, blog_lang, blog_date, blog_title_url + '.md'), 'w')
                f.write(blog_content.strip() + '\n')
                print(f'Update {blog_lang}/{blog_date}/{blog_title_url}')
