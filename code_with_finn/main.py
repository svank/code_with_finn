import IPython
from IPython.display import display
from PIL import Image

import os


_path = os.path.dirname(os.path.abspath(__file__))
_path = os.path.join(_path, "data")

_real_IPython_showtraceback = \
        IPython.core.interactiveshell.InteractiveShell.showtraceback

def code_with_finn_except_hook(*args, **kwargs):
    path = os.path.join(_path, 'error.jpg')
    display(Image.open(path))
    _real_IPython_showtraceback(*args, **kwargs)

IPython.core.interactiveshell.InteractiveShell.showtraceback = \
        code_with_finn_except_hook
