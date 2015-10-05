from initxyz.vars import xyzconfigdir
from initxyz.vcs import git_repo
from initxyz.utils import mkdir, symlink_and_move_old_to_backup, write_file
from initxyz.session import SessionPlugin
from os.path import expanduser, join
from io import StringIO

class Emacs(SessionPlugin):
    def __init__(self, session):
        super().__init__(session)
        self.path = []
        self.includes = []

    def enable(self):
        self.session.add_end_func(self._generate_init)

    def append_path(self, path):
        self.path.append(path)

    def package(self, url, name=None, lock_version=True):
        name = name or url.split('/')[-1]
        base = '~/.initxyz/emacs-packages'
        mkdir(expanduser(base))
        path = base + '/' + name

        git_repo(path, url, lock_version=lock_version)
        self.append_path(path)

    def include(self, path):
        self.includes.append(path)

    def _generate_init(self):
        loc = expanduser('~/.initxyz/var/init.el')
        symlink_and_move_old_to_backup(expanduser('~/.emacs'), loc)

        write_file(path=loc, data=self._make_content())

    def _make_content(self):
        out = StringIO()

        out.write('; Generated by init.xyz. Do not edit.\n')
        for fn in self.path:
            out.write('(add-to-list \'load-path "%s")\n' % fn)
        out.write('\n')

        for name in self.includes:
            out.write('(load "%s")\n' % join(xyzconfigdir, name))

        return out.getvalue()

emacs = Emacs.dynamic_instance()