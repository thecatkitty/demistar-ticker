import config

if config.LOCAL['language'] == 'pl':
    from .pl import *
else:
    from .en import *
