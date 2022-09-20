import os
import sys


base_path = sys.argv[1]


def covert_content(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code in [12288, 160]:
                inside_code = 32
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)


if __name__ == '__main__':
    for lang in ['zh', 'en']:
        for path,dir_list,file_list in os.walk(f'{base_path}/{lang}'):
            for file_name in file_list:
                if not file_name.endswith('.md'):
                    continue
                
                markdown_file = os.path.join(path, file_name)
                with open(markdown_file, 'r') as f:
                    content = covert_content(f.read())
                with open(markdown_file, 'w') as f:
                    f.write(content)
