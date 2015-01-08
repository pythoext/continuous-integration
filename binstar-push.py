import os
import glob
import subprocess
import traceback
from config import BRANCH_TO_CHANNEL
token = os.environ['BINSTAR_TOKEN']
cmd = ['binstar', '-t', token, 'upload']

# SET CHANNEL
try:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    BRANCH_TO_BUILD = open(os.path.join(BASE_DIR, 'build_trigger_branch'), 'r').read().strip()
except IOError:
    BRANCH_TO_BUILD = "master"

if "master" not in BRANCH_TO_BUILD:
    cmd.extend(['--channel=%s' % BRANCH_TO_CHANNEL.get(BRANCH_TO_BUILD, BRANCH_TO_BUILD)])

cmd.extend(['--force'])
cmd.extend(glob.glob('*.tar.bz2'))
try:
    subprocess.check_call(cmd)
except subprocess.CalledProcessError:
    traceback.print_exc()

