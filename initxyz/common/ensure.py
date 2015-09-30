from os.path import join, dirname, basename, realpath, expanduser
from subprocess import check_call, call, check_output
from platform import linux_distribution
from initxyz.core import add_profile
from initxyz.utils import hostname, execfile, execfile_if_exists
from initxyz.zsh import zsh
from initxyz.apt import apt
from initxyz.vcs import git_repo

from initxyz.common.ensure_misc import mkdir, update_alternatives
