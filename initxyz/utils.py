from initxyz.vars import xyzdir

import sys
import os
import shutil
import binascii
import platform
import re

def rand_hex(l=8):
    return binascii.hexlify(os.urandom(l)).decode()

def as_bytes(s):
    if isinstance(s, bytes):
        return s
    elif isinstance(s, str):
        return s.encode('utf8')
    else:
        raise TypeError('as_bytes expects bytes or str, got %r' % type(s))

def write_file(path, data):
    tmp = path + '.' + rand_hex() + '~'
    with open(tmp, 'wb') as f:
        f.write(as_bytes(data))
    os.rename(tmp, path)

def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def symlink_force(src, dst):
    if os.path.islink(dst):
        os.unlink(dst)
    os.symlink(src, dst)

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def warn(txt):
    print(colors.WARNING + 'WARN: ' + colors.RESET + txt + colors.RESET)

def info(txt):
    print(colors.OKBLUE + 'INFO: ' + colors.RESET + txt + colors.RESET)

def ask_yes_no(question, default=False):
    prefix = colors.OKGREEN + 'QUESTION: ' + colors.RESET
    while True:
        response = input(prefix + question + ' ' + ('(Y/n)' if default else '(y/N)') + ': ')
        resp = response.strip().lower()
        if resp.startswith('y'):
            return True
        if resp.startswith('n'):
            return False
        if not resp:
            return default

def move_to_backup(path):
    if os.path.isdir(path):
        raise OSError('%r is a directory' % path)
    backup_name = rand_hex() + '_' + os.path.basename(path)
    backup_dir = xyzdir + '/backups/'
    mkdir(backup_dir)
    shutil.move(path, backup_dir + backup_name)

def symlink_and_move_old_to_backup(src, dst):
    try:
        if os.readlink(src) == dst:
            return
    except OSError:
        pass

    if os.path.exists(dst):
        move_to_backup(dst)

    os.symlink(src, dst)

def hostname():
    fqdn = platform.node()

    if not re.match('^[a-zA-Z0-9._-]+$', fqdn):
        raise ValueError('invalid hostname %r' % fqdn)

    return fqdn

def execfile(name, depth=1):
    frame = sys._getframe(depth)
    with open(name, 'r') as f:
        code = compile(f.read(), name, 'exec')
        exec(code, frame.f_globals, frame.f_locals)

def execfile_if_exists(name, depth=1):
    if os.path.exists(name):
        execfile(name, depth + 1)

class ObjectRedirector:
    def __init__(self, target_func):
        object.__setattr__(self, '_target', target_func)

    def __getattr__(self, name):
        return getattr(self._target(), name)

    def _set_target_func(self, target):
        object.__setattr__(self, '_target', target)

    def _set_target(self, target):
        self._set_target_func(lambda: target)

    def __setattr__(self, k, v):
        self._target().__setattr__(k, v)

    def __repr__(self):
        return '<ObjectRedirector target: %r>' % self._target

class cached_property(object):
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value
