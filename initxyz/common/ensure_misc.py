from os.path import expanduser, exists as _exists
from os import readlink, symlink as _symlink
from subprocess import check_call, PIPE, Popen, CalledProcessError
from initxyz.utils import mkdir as _mkdir, as_bytes

def symlink(src, dst):
    try:
        if readlink(expanduser(dst)) == expanduser(src):
            return
    except OSError:
        pass
        
    _symlink(expanduser(src), expanduser(dst))

def exists(path):
    return _exists(expanduser(path))
    
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

def dconf_load(path, data):
    proc = Popen(['dconf', 'load', path], stdin=PIPE)
    proc.stdin.write(as_bytes(data))
    proc.stdin.close()
    if proc.wait() != 0:
        raise CalledProcessError('dconf load failed')
