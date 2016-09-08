import os
import requests

BASE_DIR = os.getcwd()

url = open(os.path.join(BASE_DIR, 'url')).read().strip()
src_file_path = os.path.join(BASE_DIR, 'src.zip')

f = open(src_file_path, "wb")
r = requests.get(url)
f.write(r.content)
f.close()
