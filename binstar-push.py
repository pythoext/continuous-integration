import os
import glob
import subprocess
import traceback

token = os.environ['BINSTAR_TOKEN']
cmd = ['binstar', '-t', token, 'upload']
channel = os.environ.get('BINSTAR_CHANNEL', None)
if channel is not None:
    cmd.extend(['-c %s' % channel])
cmd.extend(['--force'])
cmd.extend(glob.glob('*.tar.bz2'))
try:
    subprocess.check_call(cmd)
except subprocess.CalledProcessError:
    traceback.print_exc()

