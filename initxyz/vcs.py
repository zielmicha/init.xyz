from os.path import expanduser, exists
from subprocess import check_call, check_output
from initxyz.configfile import ConfigFile
from initxyz.vars import xyzconfigdir
from initxyz.utils import info

lock_file = ConfigFile(xyzconfigdir + '/lockfile.ini')

def git_repo(path, url, checkout=None, lock_version=False):
    expanded_path = expanduser(path)
    just_cloned = False

    if not exists(expanded_path):
        just_cloned = True
        info('cloning %s to %s' % (url, path))
        check_call(['git', 'clone', url, expanded_path])

    locked_version = None

    if lock_version:
        locked_version = lock_file.get('git', path, fallback=None)
        if locked_version:
            checkout = locked_version

    if checkout and (just_cloned or lock_version):
        current_checkout = git_get_current_checkout(expanded_path)
        if checkout != current_checkout or current_checkout is None:
            info("checking out %s at %s" % (checkout, path))
            check_call(['git', 'checkout', '--quiet', checkout], cwd=expanded_path)

    if lock_version:
        new_version = check_output(['git', 'rev-parse', '--verify', 'HEAD'], cwd=expanded_path).strip().decode()
        if new_version != locked_version:
            info("locked %s to version %s" % (path, new_version))
            lock_file.set('git', path, new_version)

def git_get_current_checkout(repo):
    try:
        data = open(repo + '/.git/HEAD').read().strip()
        if data.startswith('ref: refs/heads/'):
            return data.split('/', 2)[2]
        else:
            return data
    except IOError:
        return None
