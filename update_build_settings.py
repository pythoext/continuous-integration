
import os

try:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    BRANCH_TO_BUILD = open(os.path.join(BASE_DIR, 'build_trigger_branch'), 'r').read().strip()
    os.environ["BRANCH_TO_BUILD"] = BRANCH_TO_BUILD
except IOError:
    os.environ["BRANCH_TO_BUILD"] = "master"

print os.environ["BRANCH_TO_BUILD"]