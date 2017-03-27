from bradata.connection import Connection
from bradata.utils import _must_contain, _treat_inputs, _unzip, _set_download_directory
from bradata.tse.utils_tse import unzip_tse

import os


class Candidatos:
    """
    Download, organize and pre-process candidatos data from TSE

    http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais
    """

    def download(self, type=None, year=None):
        """
        Download a certain type of data from a year in the Candidatos option

        You can also get several years or types, just pass a list

        Types can be:
                - candidatos
                - bens
                - legendas
                - vagas

        This method covers the following years: 2016, 2014

        So, to download candidatos data from 2014, just put download(type='candidatos', ano=2015)

        Args:
            type: str or list with the type of the data
            year: str or int or list with a year

        Returns: Saves data to a local data file as ../bradata/tse/[state]/candidatos_[type]_[year].csv
        """

        _must_contain({'type': type, 'year': year}, ['type', 'year'])  # raises error if keywords do not exist

        if not isinstance(type, list):
            type = [type]

        if not isinstance(year, list):
            year = [year]

        conn = Connection()

        print('Downloading...\n')

        for t in type:
            if t == 'candidatos':
                base_url = "http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_"

            elif t == 'bens':
                base_url = "http://agencia.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_"

            elif t == 'legendas':
                base_url = "http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_legendas/consulta_legendas_"

            elif t == 'vagas':
                base_url = "http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_vagas/consulta_vagas_"

            else:

                print(t)
                raise Exception('Type should be candidatos, bens, legendas or vagas')

            print('Type: ', t)

            for y in year:

                print('Year: ', y)

                url = base_url + _treat_inputs(y) + '.zip' # treat_inputs turn int into str, raises error if diff type

                result = conn.perform_request(url, binary=True)

                if result['status'] == 'ok':
                     result = result['content']
                else:
                    print('File was not dowloaded')
                    continue

                unzip_tse(result, _set_download_directory() + '/tse')

        print('Finished')