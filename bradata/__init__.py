# -*- coding: utf-8 -*-

import pkg_resources
import bradata.utils
import bradata.agencias
import bradata.cgu
import bradata.tse

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'


__download_dir__ = bradata.utils._set_download_directory()
