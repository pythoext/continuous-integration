import os
import sys
from config import BRANCH_TO_CHANNEL, ALWAYS_BUILD_BRANCH

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

try:
    BRANCH_TO_BUILD = open(os.path.join(BASE_DIR, 'build_trigger_branch'), 'r').read().strip()
except IOError:
    BRANCH_TO_BUILD = os.environ.get('TRAVIS_BRANCH', 'master')

try:
    BUILD_NUMBER = open(os.path.join(BASE_DIR, 'build_trigger_number'), 'r').read().strip()
except IOError:
    BUILD_NUMBER = os.environ.get('TRAVIS_BUILD_NUMBER')

if 'win' in sys.platform:
    cmd = "SET"
else:
    cmd = "export"

output = "%s BRANCH_TO_BUILD=%s && %s BUILD_NUMBER=%s" % (cmd, BRANCH_TO_BUILD, cmd, BUILD_NUMBER)

if BRANCH_TO_BUILD not in ALWAYS_BUILD_BRANCH and 'trigger-ci' not in os.environ.get("TRAVIS_COMMIT_MESSAGE", ""):
    output += "%s SKIP_CI=\"SKIP_CI\"" % (cmd)

if 'master' not in BRANCH_TO_BUILD:
    # add channel if needed
    binstar_channel = BRANCH_TO_CHANNEL.get(BRANCH_TO_BUILD, BRANCH_TO_BUILD)
    output += " && conda config --add channels https://conda.anaconda.org/t/%s/prometeia/channel/%s" % (
    os.environ.get("BINSTAR_TOKEN"), binstar_channel)

output += " && anaconda config --set verify_ssl false"

print output
