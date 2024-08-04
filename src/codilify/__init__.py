__version__ = '0.0.1'

from .codilify import Codilify

def load_ipython_extension(ipython):
    ipython.register_magics(Codilify)
