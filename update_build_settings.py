import os
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

if BRANCH_TO_BUILD in BRANCH_TO_CHANNEL:
    # add channel if needed
    output += " && conda config --add channels http://conda.binstar.org/t/%s/prometeia/channel/%s" % (
    os.environ.get("BINSTAR_TOKEN"), BRANCH_TO_CHANNEL[BRANCH_TO_BUILD])

print output
