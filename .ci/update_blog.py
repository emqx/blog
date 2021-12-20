import os
import sys

import requests

base_path = sys.argv[1]
if len(sys.argv) > 2:
    changed_files = ' '.join(sys.argv[2:])
else:
    changed_files = ''


if __name__ == '__main__':
    changed_files = list(filter(lambda x: len(x.split('/')) == 3, changed_files.split()))

    update_api = os.environ.get('UPDATE_API')
    update_token = os.environ.get('UPDATE_TOKEN')
    update_status = True

    for file_name in changed_files:
        lang, _date, title = file_name.split('/')
        title = title.replace('.md', '')
        print(f'Updating {file_name}')
        if not os.path.exists(os.path.join(base_path, file_name)):
            print(f'Remove {file_name}')
            continue
        with open(os.path.join(base_path, file_name), 'r') as f:
            content = f.read()
            response = requests.put(
                url=f'{update_api}/{lang}/{title}',
                json={'contents': content},
                headers={'token': update_token}
            )
            print(response.status_code, response.text)
            if response.status_code != 200:
                update_status = False
    
    if update_status:
        print('Update blog successfully')
    else:
        sys.exit('Update blog failed')
