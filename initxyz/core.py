from initxyz.utils import execfile, info, ask_yes_no
from initxyz.vars import xyzconfigdir, xyzdir
from initxyz.session import set_current_session, Session, get_current_session
from initxyz.configfile import ConfigFile

from os import chdir
from os.path import exists

def reload():
    info('Reloading configuration')
    chdir(xyzconfigdir)
    current_session = Session()
    set_current_session(current_session)
    execfile('init.py')
    current_session.end()
    set_current_session(None)

def add_profile(name, filename=None, depth=1):
    if not filename:
        filename = 'profile_%s.py' % name

    if is_profile_enabled(name, ask=True):
        execute_profile(name, filename, depth + 1)

def execute_profile(name, filename, depth):
    session = Session(name, parent=get_current_session())
    set_current_session(session)
    execfile(filename, depth=depth + 1)
    session.end()
    set_current_session(session.parent)

profiles_config = ConfigFile(xyzdir + '/profiles.ini')

def is_profile_enabled(name, ask=False):
    if not profiles_config.has_option('profiles', name):
        if ask:
            enable = ask_yes_no('New profile %r added. Enable it now?' % name)
            set_profile_enabled(name, enable)
            return enable
        else:
            return False
    else:
        return profiles_config.get('profiles', name) == 'enabled'

def set_profile_enabled(name, enabled):
    profiles_config.set('profiles', name, 'enabled' if enabled else 'disabled')
