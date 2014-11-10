import os
import glob
import subprocess
import traceback

token = os.environ['BINSTAR_TOKEN']
channel = os.environ.get('BINSTAR_CHANNEL', 'main')
cmd = ['binstar', '-t', token, 'upload', '--force']
cmd.extend(glob.glob('*.tar.bz2'))
cmd.extend(['--channel %s' % channel])
try:
    subprocess.check_call(cmd)
except subprocess.CalledProcessError:
    traceback.print_exc()

