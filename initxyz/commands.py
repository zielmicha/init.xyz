from os.path import expanduser, exists
from shutil import copy
from initxyz.utils import mkdir, symlink_force
from initxyz.vars import xyzdir, xyzcodedir
from initxyz.core import reload, set_profile_enabled

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
        parser.add_argument('--silent', action='store_true', default=False)

    @classmethod
    def run(self, ns):
        reload(silent=ns.silent)

class Enable:
    name = 'enable'

    @classmethod
    def make_parser(self, parser):
        parser.add_argument('profile_name')

    @classmethod
    def run(self, ns):
        set_profile_enabled(ns.profile_name, True)

class Disable:
    name = 'disable'

    @classmethod
    def make_parser(self, parser):
        parser.add_argument('profile_name')

    @classmethod
    def run(self, ns):
        set_profile_enabled(ns.profile_name, False)

commands = [Init, Reload, Enable, Disable]
