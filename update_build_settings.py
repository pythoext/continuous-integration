
import os
import sys

try:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    BRANCH_TO_BUILD = open(os.path.join(BASE_DIR, 'build_trigger_branch'), 'r').read().strip()
except IOError:
    BRANCH_TO_BUILD = "master"

if 'win' in sys.platform:
    cmd = "SET"
else:
    cmd = "export"

print "%s BRANCH_TO_BUILD=%s" % (cmd, BRANCH_TO_BUILD)
