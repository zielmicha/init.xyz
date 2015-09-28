from os.path import expanduser, exists
from shutil import copy
from initxyz.utils import mkdir, symlink_force
from initxyz.vars import xyzdir, xyzcodedir
from initxyz.core import reload

class Init:
    name = 'init'

    @classmethod
    def make_parser(self, parser):
        parser.add_argument('configs_dir')

    @classmethod
    def run(self, ns):
        mkdir(xyzdir)
        symlink_force(ns.configs_dir, xyzdir + '/configs')

        init_path = xyzdir + '/configs/init.py'

        if not exists(init_path):
            copy(xyzcodedir + '/example_init.py', init_path)

class Reload:
    name = 'reload'

    @classmethod
    def make_parser(self, parser):
        pass

    @classmethod
    def run(self, ns):
        reload()

commands = [Init, Reload]
