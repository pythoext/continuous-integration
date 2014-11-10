import os
import glob
import subprocess
import traceback

token = os.environ['BINSTAR_TOKEN']
channel = os.environ.get('BINSTAR_CHANNEL', 'main')
cmd = ['binstar', '-t', token, 'upload', '--force', '--channel %s' % channel]
cmd.extend(glob.glob('*.tar.bz2'))
try:
    subprocess.check_call(cmd)
except subprocess.CalledProcessError:
    traceback.print_exc()

