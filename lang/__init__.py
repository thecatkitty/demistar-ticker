import config

if config.LANG == 'pl':
    from .pl import *
else:
    from .en import *
