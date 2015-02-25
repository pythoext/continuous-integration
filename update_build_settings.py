import os
import yaml
import sys
from config import BRANCH_TO_CHANNEL

try:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    BRANCH_TO_BUILD = open(os.path.join(BASE_DIR, 'build_trigger_branch'), 'r').read().strip()
except IOError:
    BRANCH_TO_BUILD = "master"

if 'win' in sys.platform:
    cmd = "SET"
else:
    cmd = "export"

output = "%s BRANCH_TO_BUILD=%s" % (cmd, BRANCH_TO_BUILD)

if 'master' not in BRANCH_TO_BUILD:
    # add channel if needed
    binstar_channel = BRANCH_TO_CHANNEL.get(BRANCH_TO_BUILD, BRANCH_TO_BUILD)
    output += " && conda config --add channels https://conda.binstar.org/t/%s/prometeia/channel/%s" % (
    os.environ.get("BINSTAR_TOKEN"), binstar_channel)

    # update meta.yaml requirements
    custom_meta_path = os.path.join('..', 'conda-recipe', "%s.yaml" % binstar_channel)
    if os.path.exists(custom_meta_path):
        package_meta_path = os.path.join('..', 'conda-recipe', "meta.yaml")

        package_meta = yaml.load(open(package_meta_path, "rb"))
        custom_meta = yaml.load(open(custom_meta_path, "rb"))

        for r in custom_meta['requirements']['run']:
            package_meta['requirements']['run'].append(r)
        yaml.dump(package_meta, open(package_meta_path, "wb"), default_flow_style=False)

output += " && binstar config --set verify_ssl false"

print output
