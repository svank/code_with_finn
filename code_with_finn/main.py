try:
    import IPython
    from IPython.display import display
except:
    # We must not be in IPython?
    import warnings
    warnings.warn("code_with_finn could not load IPython")

try:
    from PIL import Image
except:
    import warnings
    warnings.warn("code_with_finn could not load pillow")


import contextlib
import os
import sys
import traceback


_path = os.path.dirname(os.path.abspath(__file__))
_path = os.path.join(_path, "data")


_has_excepted = False
_suppress_outputs = False


def _code_with_finn_except_hook(*args, **kwargs):
    if not _suppress_outputs and in_notebook():
        t = sys.exc_info()[2]
        depth = len(traceback.format_list(traceback.extract_tb(t)))
        if depth > 5:
            file = 'bad_error.jpg'
        else:
            file = 'error.jpg'
        path = os.path.join(_path, file)
        try:
            display(Image.open(path))
        except:
            pass
    
    try:
        _real_IPython_showtraceback(*args, **kwargs)
    except:
        pass
    
    global _has_excepted
    _has_excepted = True


def _activate_error_messages():
    global _real_IPython_showtraceback
    try:
        _real_IPython_showtraceback = \
                IPython.core.interactiveshell.InteractiveShell.showtraceback
        IPython.core.interactiveshell.InteractiveShell.showtraceback = \
                _code_with_finn_except_hook
    except:
        pass


def _deactivate_error_messages():
    try:
        IPython.core.interactiveshell.InteractiveShell.showtraceback = \
                _real_IPython_showtraceback
    except:
        pass


def announce_errors(activate=True):
    if activate:
        _activate_error_messages()
    else:
        _deactivate_error_messages()


announce_errors(True)


def _code_with_finn_pre_run_cell():
    # Ensure we start cell execution with the exception flag cleared
    global _has_excepted, _suppress_outputs
    _has_excepted = False
    _suppress_outputs = False


try:
    ip = IPython.get_ipython()
    ip.events.register('pre_run_cell', _code_with_finn_pre_run_cell)
except:
    pass


def _code_with_finn_post_run_cell():
    # Ensure we only show the success message if there was no exception
    global _has_excepted
    if _has_excepted or _suppress_outputs or not in_notebook():
        _has_excepted = False
        return
    path = os.path.join(_path, 'success.jpg')
    try:
        display(Image.open(path))
    except:
        pass


def _activate_success_messages():
    global _suppress_success
    _suppress_success = False
    try:
        ip = IPython.get_ipython()
        ip.events.register('post_run_cell', _code_with_finn_post_run_cell)
    except:
        pass


def _deactivate_success_messages():
    try:
        ip = IPython.get_ipython()
        ip.events.unregister('post_run_cell', _code_with_finn_post_run_cell)
    except:
        pass


def celebrate_success(activate=True):
    if activate:
        _activate_success_messages()
    else:
        _deactivate_success_messages()


@contextlib.contextmanager
def out_finn():
    global _suppress_outputs
    _suppress_outputs = True
    yield
    _suppress_outputs = False


def in_notebook():
    try:
        from IPython import get_ipython
        if 'IPKernelApp' not in get_ipython().config:
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True
