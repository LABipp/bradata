from bradata.connection import Connection
import requests
from bs4 import BeautifulSoup
import time

class Statistics:

    def get_links(self, xml):
        """
        Get all links from a html page
        :param xml: string of a html page
        :return: links: A list of all the link in the page
        """
        soup = BeautifulSoup(xml, 'lxml')
        links = soup("a")

        return links

    def get_infraero(self, year="2015"):

        """
        Get all statistics xls files from Infraero website for a given year
        :param year: string year, from 2017 to 2012
        :return: links: A list of all the links downloaded
        """

        database_links = set()
        conn = Connection()
        statistics_page = conn.perform_request("http://www.infraero.gov.br/index.php/br/estatisticas/estatisticas.html")
        links = self.get_links(statistics_page["content"])

        for link in links:
            if (('Estatistica' in link['href']) and (year in link['href'])):
                file_name = str(link)
                file_name = file_name.split('"')[1]
                complete_link = "http://www.infraero.gov.br" + str(file_name)
                database_links.add(complete_link)

        for link in database_links:
            name = str.split(link, "/")[-1]
            print("Downloading: ", link)
            resp = requests.get(link)
            output = open(year + "_" + str(name), 'wb')
            output.write(resp.content)
            output.close()

            time.sleep(0.05)

        return database_links

