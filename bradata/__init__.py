# -*- coding: utf-8 -*-
import pkg_resources
import bradata.utils

from .infraero import Infraero

from .infraero import Infraero

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

__download_dir__ = bradata.utils.set_download_directory()
