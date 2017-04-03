import bradata
from bradata.cgu.ceis import get as ceis_get
from bradata.connection import stale_url_warning
import requests
import os
import datetime
import zipfile
import io


def get(date=None):
    """
    gets CEPIM (Cadastro de Entidades sem Fins Lucrativos Impedidas, http://www.portaldatransparencia.gov.br/cepim) data. it
    converts the csv encoding to utf8.
    :param date: a datetime object with year, month, and day attributes. if not provided, will get current day (be
    careful if on other timezone than Brasília). input can be constructed by 
    importing datetime module and typing `datetime.date(1994, 07, 18)`. 
    :return: downloads csv to directory bradata.__download_dir__
    """
    # check bradata.cgu.ceis for source code.
    return ceis_get(date=date, cadastro='CEPIM')
