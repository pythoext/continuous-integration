import os
import sys
import glob
import subprocess
import traceback
from config import BRANCH_TO_CHANNEL

def execcmd(message, cmdlist, exitcode=None):
    print message
    try:
        subprocess.check_call(cmdlist)
        print "Done!"
        return True
    except subprocess.CalledProcessError:
        print cmd
        traceback.print_exc()
        if exitcode is not None:
            sys.exit(exitcode)
        return False


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
    cmd.append('--channel=%s' % target_channel)

uploadus = sorted(glob.glob('*.tar.bz2'))
cmd.extend(['--force'] + uploadus)
execcmd("Uploading on Anaconda channel %s of packages %s" % (target_channel, ', '.join(uploadus)), cmd, 1)

## Aggiunta per produrre la label mobile basata sulla verisone
if target_channel and len(uploadus) == 1:
    ok = execcmd("Installing anaconda-client", ['conda', 'install', 'anaconda-client'])
    if not ok:
        execcmd("Upgrading anaconda-client to use the new api", ['conda', 'update', 'anaconda-client'], 3)
    # Naming del tipo: "gsf-4.1.2-np110py27_2025.tar.bz2"
    versione = uploadus.pop().split('-')[1]
    major, minor, patch = versione.split('.')
    ver_channel = '%s_%s_%s' % (target_channel, major.zfill(2), minor.zfill(2))
    execcmd("Copying label %s into %s" % (target_channel, ver_channel),
            ['anaconda', '-t', token, 'label', '--copy', target_channel, ver_channel], 3)
