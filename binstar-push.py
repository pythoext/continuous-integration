import os
import glob
import subprocess
import traceback

token = os.environ['BINSTAR_TOKEN']
cmd = ['binstar', '-t', token, 'upload']

# SET CHANNEL
try:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    BRANCH_TO_BUILD = open(os.path.join(BASE_DIR, 'build_trigger_branch'), 'r').read().strip()
except IOError:
    BRANCH_TO_BUILD = "master"
branch_to_channel = {
    'develop': 'dev',
    'ratingpro': 'ratingpro2',
    'tg_dj_oo': 'new-ui'
}
if BRANCH_TO_BUILD in branch_to_channel:
    cmd.extend(['--channel=%s' % branch_to_channel[BRANCH_TO_BUILD]])

cmd.extend(['--force'])
cmd.extend(glob.glob('*.tar.bz2'))
try:
    subprocess.check_call(cmd)
except subprocess.CalledProcessError:
    traceback.print_exc()

