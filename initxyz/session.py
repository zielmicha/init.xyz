from initxyz.utils import ObjectRedirector
import functools

_current_session = None

def get_current_session():
    return _current_session

def set_current_session(session):
    global _current_session
    _current_session = session

class Session:
    def __init__(self):
        self._end_funcs = []
        self.parent = None
        self.name = 'root'

    def is_root(self):
        return self.parent is None

    def assert_root(self):
        if not self.is_root():
            raise ValueError('this operation doesn\'t make sense on non-root session')

    def add_end_func(self, func):
        self._end_funcs.append(func)

    def end(self):
        for func in reversed(self._end_funcs):
            func()

class SessionPlugin:
    def __init__(self, session):
        self.session = session

    @classmethod
    def get(cls, session):
        name = '_' + cls.__module__ + '_' + cls.__name__
        if not hasattr(session, name):
            setattr(session, name, cls(session))
        return getattr(session, name)

    @classmethod
    def make_method(cls, name):
        @functools.wraps(getattr(cls, name))
        def func(*args, **kwargs):
            return getattr(cls.get(current_session), name)(*args, **kwargs)

        return func

    @classmethod
    def dynamic_instance(cls):
        return ObjectRedirector(lambda: cls.get(get_current_session()))
