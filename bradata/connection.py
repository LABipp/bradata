import requests
import time
from bs4 import BeautifulSoup
import requests

class Connection():
    """
    Class that handle connections
    """

    def perform_request(self, url, n_of_tentatives=5):
        """
        Perform a request handling exception and server errors printing status

        :param url: string
        :param n_of_tentatives: int
        :return: dict :: status : ok/error, content: xml/url, [error_type, error_desc] if error
        """

        count = 0
        while 1:
            try:
                print('Fetch {}'.format(url))

                #fetch_time = time.time()
                req = requests.get(url, timeout=60)
                #fetch_time = time.time() - fetch_time

                status = req.status_code
                if status != 200:
                    print('ERROR {}. {}'.format(req.status_code, req.text))
                    time.sleep(5)

                    count += 1
                    if count > n_of_tentatives:
                        print('Too many errors in a row. Returned: ERROR {}'.format(req.status_code))
                        return {'status': 'error', 'error_type': req.status_code, 'error_desc': req.text, 'content': url}

                    print('Trying Again...')
                    continue

                else:
                    return {'status': 'ok', 'content': req.text}

            except Exception as e:

                print('EXCEPTION {}'.format(e))

                count += 1
                if count > n_of_tentatives:
                    print('Too many exceptions in a row. Returned: ERROR EXC')
                    return {'status': 'error', 'error_type': 'exception', 'error_desc': e, 'content': url}

                time.sleep(5)
                print('Trying Again...')
                continue

def get_links(xml):
    """
    Get all links from a html page
    :param xml: string of a html page
    :return: links: A list of all the link in the page
    """
    soup = BeautifulSoup(xml, 'lxml')
    links = soup("a")

    return links

def get_infraero(year="2015"):


    database_links = set()
    conn = Connection()
    statistics_page = conn.perform_request("http://www.infraero.gov.br/index.php/br/estatisticas/estatisticas.html")
    links = get_links(statistics_page["content"])
    for link in links:
        if (('Estatistica' in link['href']) and (year in link['href'])):
            link2 = str(link)
            link2 = link2.split('"')[1]
            complete_link = "http://www.infraero.gov.br" + str(link2)
            database_links.add(complete_link)

    for link in database_links:
        name = str.split(link,"/")[-1]
        print("Downloading: ", link)
        resp = requests.get(link)
        output = open(year + "_" + str(name), 'wb')
        output.write(resp.content)
        output.close()

        time.sleep(0.05)

    return database_links

aa = get_infraero()

