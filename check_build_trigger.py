import os
import sys
from config import ALWAYS_BUILD_BRANCH

BRANCH_TO_BUILD = os.environ.get('TRAVIS_BRANCH', 'master')

if 'win' in sys.platform:
    cmd = "SET"
else:
    cmd = "export"

if BRANCH_TO_BUILD not in ALWAYS_BUILD_BRANCH and 'trigger-ci' not in os.environ.get("TRAVIS_COMMIT_MESSAGE", ""):
    output = " %s SKIP_CI=\"SKIP_CI\"" % cmd
else:
    output = ""

print output



