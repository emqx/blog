import os
import sys
import time

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
        file_split = file_name.split('/')
        if len(file_split) != 3:
            continue
        lang, _date, title = file_split
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
                headers={'token': update_token},
                timeout=20
            )
            if response.status_code == 200:
                print(f'Updated {file_name}')
            elif response.status_code == 404:
                print(f'Remove {file_name}')
            else:
                print(response.status_code, response.text)
                update_status = False
            time.sleep(2)

    if update_status:
        print('Update blog successfully')
    else:
        sys.exit('Update blog failed')
