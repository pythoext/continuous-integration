import sys
import json
import os
import argparse
import logging
import shutil


class Repacker(object):
    """A coda offline repacker"""

    def __init__(self, mainrepo, envinfofile="envinfo.json", skipfirstfolder=True):
        self.mainrepo = mainrepo
        self.skipfirstfolder = bool(skipfirstfolder)
        with open(envinfofile) as envfile:
            self.envinfo = json.load(envfile)

    @property
    def distro(self):
        return self.envinfo["env_vars"]["CONDA_DEFAULT_ENV"]

    @property
    def platform(self):
        return self.envinfo['platform']

    @property
    def pkgs_dirs(self):
        return [os.path.abspath(d) for d in self.envinfo['pkgs_dirs']][int(self.skipfirstfolder):]
        

    @property
    def target(self):
        return os.path.abspath(os.path.join(self.mainrepo, self.distro, self.platform))

    def bootstrap(self):
        """Upsert of base distro structure"""
        def _makeme(*args):
            target = os.path.normpath(os.path.join(self.target, *args))
            if not os.path.isdir(target):
                logging.info("Creating %s", target)
                os.makedirs(target)
            else:
                logging.info("Folder %s already exists", target)
        _makeme()
        _makeme('..', 'noarch')

    @staticmethod
    def list_pkgs(packdir):
        """Return the dict of packages in given path"""
        found = {}
        for fname in os.listdir(packdir):
            fullname = os.path.join(packdir, fname)
            if os.path.isfile(fullname) and fname.endswith('.tar.bz2'):
                found[fname] = fullname
        return found

    def sync(self, force=False, clean=True):
        """Syncronize the packages in main repo folder to the required"""
        logging.info("Syncing %s", self.target)
        required = {}
        for packdir in self.pkgs_dirs:
            required.update(self.list_pkgs(packdir))
        existing = self.list_pkgs(self.target)
        obsolete = set(existing) - set(required)
        if obsolete and clean:
            for removeme in sorted(existing[o] for o in obsolete):
                logging.info("Removing obsolete package %s", removeme)
                os.remove(removeme)
        elif obsolete:
            for removeme in sorted(existing[o] for o in obsolete):
                logging.info("Obsolete package %s left in folder", removeme)
        else:
            logging.info("No obsolete package to remove")
        copyus = set(required)
        if not force:
            copyus -= set(existing)
        if copyus:
            for copyme in sorted(required[o] for o in copyus):
                logging.info("Copying package %s", copyme)
                shutil.copy(copyme, self.target)
        else:
            logging.info("No new package is required")


def main():
    """Main"""
    logging.basicConfig(format='%(asctime)-15s - %(levelname)s - %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser(description='Offline Anaconda repacker')
    parser.add_argument('mainrepopath', help='Path to main offline distro repository')
    parser.add_argument('-f', '--force', help='Overwrite existing packages', action='store_true', default=False)
    parser.add_argument('-nc', '--noclean', help='Do not remove obsolete packages', action='store_true', default=False)
    parser.add_argument('-o', '--outfile', help='Output file with target folder', default='tgfolder.txt')
    args = parser.parse_args()
    repa = Repacker(args.mainrepopath)
    repa.bootstrap()
    repa.sync(force=args.force, clean=not args.noclean)
    logging.info("Writing output folder %s into %s", repa.target, args.outfile)
    with open(args.outfile, 'w') as outfile:
        outfile.write(repa.target)

if __name__ == "__main__":
    main()
