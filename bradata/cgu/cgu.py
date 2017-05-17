from bradata.connection import _stale_url_warning
import bradata.utils
import requests
import os
import zipfile
import io
import bradata


def get_cgu_data(date, cadastro, freq, consulta=None):
    """
    gets some CGU data at http://www.portaldatransparencia.gov.br/. it is 
    wrapped by helper functions that make the library more discoverable. it 
    converts the csv encoding to utf8.

    :param date: a string in YYYY-mm-dd format or a datetime object with year, 
    month, and day attributes. if not provided, will get current day (be
    careful if on other timezone than Brasília). input can be constructed by 
    importing datetime module and typing `datetime.date(1994, 07, 18)`.
    :param cadastro: this is the database to be fetched (e.g., 'ceis')
    :param consulta: usually the same as in cadastro, but sometimes the 
    internal API calls it something else, as in the case of CEAF.
    :param freq: 'd' for daily, 'm' for monthly, 'y' or 'a' for annually.
    :return: downloads csv to directory bradata.__download_dir__
    """
    if consulta is None:  # because some consultas are not the same as cadastro
        consulta=cadastro
    freq = freq.lower()
    date = bradata.utils._parse_time(date, freq=freq)
    time_dict = {'a': ['a', 'consulta'], 'm': ['a', 'm', 'consulta'], 
                 'd': ['d', 'm', 'a', 'consulta'], 'y': ['a', 'consulta']}
    params = {'a': date.year, 'm': '{:02d}'.format(date.month), 
              'd': '{:02d}'.format(date.day), 'consulta': consulta}
    filtered_params = {key: params[key] for key in time_dict[freq]}  # removes day portion if freq='m', e.g.
    r = requests.get('http://arquivos.portaldatransparencia.gov.br/downloads.asp',
                     stream=True, params=filtered_params, timeout=1)
    if r.status_code == 200:
        request_content = io.BytesIO(r.content)
        if zipfile.is_zipfile(request_content):
            z = zipfile.ZipFile(request_content)
            filename = z.namelist()[0]
            with z.open(filename) as f:
                latin_db = f.read()
            cgu_db = latin_db.decode('cp1252').replace('\x00', '')  # http://www.portaldatransparencia.gov.br/faleConosco/perguntas-tema-download-dados.asp
            filepath = os.path.join(bradata.__download_dir__, 'CGU', filename)
            bradata.utils._create_download_subdirectory('CGU')
            with open(filepath, mode='wt', encoding='utf8') as f:
                f.write(cgu_db)
            return "{} downloaded to {}".format(cadastro, filepath)
        else:
            print('file from this date is not available. website gave\n\"\"\"\n'
                  '{}\n\"\"\"\nas a reply. please try a different date.'
                  .format(r.text))
            return None
    else:
        print(stale_url_warning.format(r.status_code, r.text, 
                                   'Portal da Transparência do Governo Federal', 
            'http://www.portaltransparencia.gov.br/downloads/snapshot.asp?c={}'
            .format(cadastro)))
        r.raise_for_status()


def get_ceis(date=None):
    """
    gets CEIS (cadastro de empresas inidôneas e suspensas, 
    http://www.portaldatransparencia.gov.br/ceis) data. it converts the csv 
    encoding to utf8.
    :param date: a string in YYYY-mm-dd format or a datetime object with year, 
    month, and day attributes. if not provided, will get current day (be
    careful if on other timezone than Brasília). input can be constructed by 
    importing datetime module and typing `datetime.date(1994, 07, 18)`. 
    :return: downloads csv to directory bradata.__download_dir__
    """
    return get_cgu_data(date=date, cadastro='CEIS', freq='d')


def get_cepim(date=None):
    """
    gets CEPIM (Cadastro de Entidades sem Fins Lucrativos Impedidas, 
    http://www.portaldatransparencia.gov.br/cepim) data. it converts the csv 
    encoding to utf8.
    :param date: a string in YYYY-mm-dd format or a datetime object with year, 
    month, and day attributes. if not provided, will get current day (be
    careful if on other timezone than Brasília). input can be constructed by 
    importing datetime module and typing `datetime.date(1994, 07, 18)`. 
    :return: downloads csv to directory bradata.__download_dir__
    """
    return get_cgu_data(date=date, cadastro='CEPIM', freq='d')


def get_cnep(date=None):
    """
    gets CNEP (Cadastro Nacional de Empresas Punidas, 
    http://www.portaldatransparencia.gov.br/cnep) data. it converts the csv 
    encoding to utf8.
    :param date: a string in YYYY-mm-dd format or a datetime object with year, 
    month, and day attributes. if not provided, will get current day (be
    careful if on other timezone than Brasília). input can be constructed by 
    importing datetime module and typing `datetime.date(1994, 07, 18)`. 
    :return: downloads csv to directory bradata.__download_dir__
    """
    return get_cgu_data(date=date, cadastro='CNEP', freq='d')

def get_ceaf(date=None):
    """
    gets CEAF (Cadastro de Expulsões da Administração Federal, 
    http://www.transparencia.gov.br/servidores/SaibaMaisPunicoes.asp) data. it
    converts the csv encoding to utf8.
    :param date: a string in YYYY-mm-dd format or a datetime object with year, 
    month, and day attributes. if not provided, will get current day (be
    careful if on other timezone than Brasília). input can be constructed by 
    importing datetime module and typing `datetime.date(1994, 07, 18)`. 
    :return: downloads csv to directory bradata.__download_dir__
    """
    return get_cgu_data(date=date, cadastro='CEAF', consulta='expulsoes', freq='d')

def get_diarias(date=None):
    """
    gets pagamentos de diárias pagas aos servidores e colaboradores eventuais 
    (http://www.portaltransparencia.gov.br/despesasdiarias/) data. it converts 
    the csv encoding to utf8.
    :param date: a string in YYYY-mm format or a datetime object with year and 
    month attributes. if not provided, will get current day (be
    careful if on other timezone than Brasília). input can be constructed by 
    importing datetime module and typing `datetime.date(1994, 07, 18)`. 
    :return: downloads csv to directory bradata.__download_dir__
    """
    return get_cgu_data(date=date, cadastro='Diarias', freq='m')
