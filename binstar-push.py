import os
import sys
import glob
import subprocess
import traceback
import logging
from config import BRANCH_TO_CHANNEL

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stderr)

def execcmd(message, cmdlist, exitcode=None):
    logging.info(message)
    try:
        subprocess.check_call(cmdlist)
        logging.debug('Done!')
        return True
    except subprocess.CalledProcessError:
        logging.warning("Failed '%s' because of: %s", ' '.join(cmdlist), traceback.format_exc())
        if exitcode is not None:
            logging.error("Exiting with %d", exitcode)
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
VESIONLABEL = False # Disabilitato, abbiamo preso altra via
if VESIONLABEL and target_channel and len(uploadus) == 1:
    ok = execcmd("Installing anaconda-client", ['conda', 'install', '-y', 'anaconda-client'])
    if not ok:
        execcmd("Upgrading anaconda-client to use the new api", ['conda', 'update', '-y', 'anaconda-client'], 3)
    # Naming del tipo: "gsf-4.1.2-np110py27_2025.tar.bz2"
    packname = uploadus.pop()
    versione = packname.split('-')[-2]
    while versione.count('.') < 2:
        versione += '.0'
    prodotto = '.'.join(packname.split('-')[:-2])
    logging.info("Calculating versiong label from label %s for product: %s v. %s", 
                 target_channel, prodotto, versione)
    major, minor, patch = versione.split('.')
    ver_channel = '%s_%s_%s' % (target_channel, major.zfill(2), minor.zfill(2))
    execcmd("Copying label %s into %s" % (target_channel, ver_channel),
            ['anaconda', '-t', token, 'label', '--copy', target_channel, ver_channel], 3)
