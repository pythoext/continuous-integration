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
    output += " && conda config --add channels http://conda.binstar.org/t/%s/prometeia/channel/%s" % (
    os.environ.get("BINSTAR_TOKEN"), binstar_channel)

    # update meta.yaml requirements
    if os.path.exists(os.path.join('..', 'conda-recipe', "%s.yaml" % binstar_channel)):
        package_meta_path = os.path.join('..', 'conda-recipe', "meta.yaml")
        package_meta = yaml.load(open(package_meta_path, "rb"))
        if binstar_channel in package_meta['requirements']:
            for r in package_meta['requirements'][binstar_channel]:
                package_meta['requirements']['run'].append(r)
            yaml.dump(package_meta, open(package_meta_path, "wb"), default_flow_style=False)

print output
