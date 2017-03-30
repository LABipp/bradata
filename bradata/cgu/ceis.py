import bradata
import requests
import os
import datetime
import zipfile
import io


def get(date=None):
    """
    gets CEIS (cadastro de empresas inidôneas e suspensas, http://www.portaldatransparencia.gov.br/ceis) data. it
    converts the csv encoding to utf8.
    :param date: a datetime object with year, month, and day attributes. if not provided, will get current day (be
    careful if on other timezone than Brasília). input can be constructed by typing `datetime.date(1994, 07, 18)`. 
    :return: downloads csv to bradata.__download_dir__ directory.
    """
    if date is None:
        date = datetime.datetime.now()
    params = {'a': date.year, 'm': '{:02d}'.format(date.month), 'd': '{:02d}'.format(date.day), 'consulta': 'CEIS'}
    r = requests.get('http://arquivos.portaldatransparencia.gov.br/downloads.asp', stream=True, params=params, timeout=1)
    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        filename = z.namelist()[0]
        with z.open(filename) as f:
            latinceis = f.read()
        ceis = latinceis.decode('cp1252').replace('\x00', '')  # http://www.portaldatransparencia.gov.br/faleConosco/perguntas-tema-download-dados.asp
        with open(os.path.join(bradata.__download_dir__, filename), mode='wt', encoding='utf8') as f:
            f.write(ceis)
        return "CEIS downloaded to {}".format(bradata.__download_dir__)
    else:
        r.raise_for_status()
