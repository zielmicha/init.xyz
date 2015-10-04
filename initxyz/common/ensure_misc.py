from os.path import expanduser
from os import readlink
from subprocess import check_call
from initxyz.utils import mkdir as _mkdir

def mkdir(path):
    _mkdir(expanduser(path))

def update_alternatives(name, target):
    if not check_alternative(name, target):
        check_call(['sudo', 'update-alternatives', '--set', name, target])

def check_alternative(name, target):
    try:
        return readlink('/etc/alternatives/' + name) == target
    except OSError:
        return False
