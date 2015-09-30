from os.path import join, dirname, basename, realpath, expanduser
from platform import linux_distribution
from initxyz.core import add_profile
from initxyz.utils import hostname, execfile, execfile_if_exists
from initxyz.zsh import zsh
from initxyz.apt import apt
from initxyz.vcs import git_repo

from initxyz.utils import mkdir as _mkdir

def mkdir(path):
    _mkdir(expanduser(path))
