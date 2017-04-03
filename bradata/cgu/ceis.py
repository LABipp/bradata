import bradata
from bradata.connection import stale_url_warning
import requests
import os
import datetime
import zipfile
import io


def get(date=None, cadastro='CEIS'):
    """
    gets CEIS (cadastro de empresas inidôneas e suspensas, http://www.portaldatransparencia.gov.br/ceis) data. it
    converts the csv encoding to utf8.
    :param date: a datetime object with year, month, and day attributes. if not provided, will get current day (be
    careful if on other timezone than Brasília). input can be constructed by 
    importing datetime module and typing `datetime.date(1994, 07, 18)`. 
    :return: downloads csv to directory bradata.__download_dir__
    """
    if date is None:
        date = datetime.datetime.now()
    params = {'a': date.year, 'm': '{:02d}'.format(date.month), 'd': '{:02d}'.format(date.day), 'consulta': cadastro}
    r = requests.get('http://arquivos.portaldatransparencia.gov.br/downloads.asp', stream=True, params=params, timeout=1)
    if r.status_code == 200:
        request_content = io.BytesIO(r.content)
        if zipfile.is_zipfile(request_content):
            z = zipfile.ZipFile(request_content)
            filename = z.namelist()[0]
            with z.open(filename) as f:
                latinceis = f.read()
            ceis = latinceis.decode('cp1252').replace('\x00', '')  # http://www.portaldatransparencia.gov.br/faleConosco/perguntas-tema-download-dados.asp
            filepath = os.path.join(bradata.__download_dir__, filename)
            with open(filepath, mode='wt', encoding='utf8') as f:
                f.write(ceis)
            return "CEIS downloaded to {}".format(filepath)
        else:
            return "file from this date is not available. website gave\"\"\" {}\"\"\" as a reply. please try a different date.".format(r.text)  # stopped here
    else:
        print(stale_url_warning.format(r.status_code, r.text, 'Portal da Transparência do Governo Federal', 'http://www.portaltransparencia.gov.br/downloads/snapshot.asp?c=CEIS'))
        r.raise_for_status()
