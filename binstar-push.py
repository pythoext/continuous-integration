import os
import sys
import glob
import subprocess
import traceback
from config import BRANCH_TO_CHANNEL
token = os.environ['BINSTAR_TOKEN']
cmd = ['binstar', '-t', token, 'upload']

target_channel = None

if len(sys.argv) > 1:
    target_channel = sys.argv[1]
else:
    # SET CHANNEL
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        BRANCH_TO_BUILD = open(os.path.join(BASE_DIR, 'build_trigger_branch'), 'r').read().strip()
        target_channel = BRANCH_TO_CHANNEL.get(BRANCH_TO_BUILD, BRANCH_TO_BUILD)
    except IOError:
        target_channel = None

if target_channel is not None:
    cmd.extend(['--channel=%s' % target_channel ])

cmd.extend(['--force'])
cmd.extend(glob.glob('*.tar.bz2'))

try:
    subprocess.check_call(cmd)
except subprocess.CalledProcessError:
    traceback.print_exc()

