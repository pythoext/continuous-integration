import sys
import os
import zipfile
import requests

# usage download_extract_zip path/to/extract/folder

BASE_DIR = os.getcwd()

dest_dir = sys.argv[1]

if not os.path.isabs(dest_dir):
    dest_dir = os.path.join(BASE_DIR, dest_dir)

if not os.path.exists(dest_dir):
    raise RuntimeError("Destination path path not found: %s" % dest_dir)

url = open(os.path.join(BASE_DIR, 'url')).read().strip()
src_file_path = os.path.join(BASE_DIR, 'src.zip')

f = open(src_file_path, "wb")
r = requests.get(url)
f.write(r.content)
f.close()

print "Extract everythig from %s to %s" % (src_file_path, dest_dir)

z = zipfile.ZipFile(src_file_path, "r", compression=zipfile.ZIP_STORED, allowZip64=True)
z.extractall(dest_dir)

print "OK"
sys.exit(0)