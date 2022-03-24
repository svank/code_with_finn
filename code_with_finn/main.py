try:
    import IPython
    from IPython.display import display
    from PIL import Image
except:
    pass

import os
import sys


_path = os.path.dirname(os.path.abspath(__file__))
_path = os.path.join(_path, "data")


_has_excepted = False


def code_with_finn_except_hook(*args, **kwargs):
    path = os.path.join(_path, 'error.jpg')
    try:
        display(Image.open(path))
        _real_IPython_showtraceback(*args, **kwargs)
    except:
        pass
    
    global _has_excepted
    _has_excepted = True


try:
    _real_IPython_showtraceback = \
            IPython.core.interactiveshell.InteractiveShell.showtraceback
    IPython.core.interactiveshell.InteractiveShell.showtraceback = \
            code_with_finn_except_hook
except:
    pass


def _code_with_finn_pre_run_cell():
    # Ensure we start cell execution with the exception flag cleared
    global _has_excepted
    _has_excepted = False


def _code_with_finn_post_run_cell():
    # Ensure we only show the celebration if there was no exception
    global _has_excepted
    if _has_excepted:
        _has_excepted = False
        return
    path = os.path.join(_path, 'success.jpg')
    try:
        display(Image.open(path))
    except:
        pass


def _activate_success_messages():
    try:
        ip = IPython.get_ipython()
        ip.events.register('post_run_cell', _code_with_finn_post_run_cell)
    except:
        pass


def celebrate_success():
    _activate_success_messages()

