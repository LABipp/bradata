# -*- coding: utf-8 -*-
import pkg_resources

from .infraero import Infraero
from .tse import Tse

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
