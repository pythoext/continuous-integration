import sys
import os
import yaml
import glob
import shutil
#try:
from conda_build.config import Config
#except ImportError:
#    from conda_build import config
config = Config()

binary_package_glob = os.path.join(config.bldpkgs_dir, '*.tar.bz2')
binary_package = sorted(glob.glob(binary_package_glob))[-1]

shutil.move(binary_package, '.')
