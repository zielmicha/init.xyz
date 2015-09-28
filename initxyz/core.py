from initxyz.utils import execfile
from initxyz.vars import xyzconfigdir
from initxyz.session import set_current_session, Session

from os import chdir

def reload():
    chdir(xyzconfigdir)
    current_session = Session()
    set_current_session(current_session)
    execfile('init.py')
    current_session.end()
    set_current_session(None)
