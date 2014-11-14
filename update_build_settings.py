
import os
import sys

branch_to_channel = {
    'develop': 'dev',
    'ratingpro': 'ratingpro2',
    'tg_dj_oo': 'new-ui'
}

try:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    BRANCH_TO_BUILD = open(os.path.join(BASE_DIR, 'build_trigger_branch'), 'r').read().strip()
except IOError:
    BRANCH_TO_BUILD = "master"

if 'win' in sys.platform:
    cmd = "SET"
else:
    cmd = "export"

out = "%s BRANCH_TO_BUILD=%s" % (cmd, BRANCH_TO_BUILD)
if BRANCH_TO_BUILD in branch_to_channel:
    out += " && %s SET BINSTAR_CHANNEL=%s" % (cmd, branch_to_channel[BRANCH_TO_BUILD])

print out