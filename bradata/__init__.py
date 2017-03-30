# -*- coding: utf-8 -*-
import bradata.agencias
import bradata.cgu
import bradata.tse
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'


__download_dir__ = bradata.utils._set_download_directory()
