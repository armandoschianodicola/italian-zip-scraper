import requests
import re

from bs4 import BeautifulSoup

from models.CityFactory import CityFactory
from models.City import City


class ItalianRegionCityFactory(CityFactory):

    def create_city_list(self):

        # get URL
        page = requests.get("https://it.wikipedia.org/wiki/{}".format(self.link))

        # scrape webpage
        soup = BeautifulSoup(page.content, 'html.parser')

        cities_table = soup.find('table')

        cities_links = cities_table.find_all('a', href=re.compile(r'/wiki/.*'))

        cities_links = filter(lambda x: "Provincia_" not in x.get('href'), cities_links)

        return list(cities_links)

    def create_city(self, city_link):

        city = requests.get("https://it.wikipedia.org/{}".format(city_link.get('href')))

        city_soup = BeautifulSoup(city.content, 'html.parser')

        info_table = city_soup.find('table', {"class": "infobox sinottico"})

        region = None
        zip_code = None
        istat_code = None

        if info_table is not None:

            region = info_table.find('th', string='Regione').next_sibling.getText()

            region = region.replace("\n", "").replace(" ", "")

            zip_code = info_table.find('th', string='Cod. postale').next_sibling.getText()

            zip_code = zip_code.replace("\n", "").replace(" ", "")

            istat_code = info_table.find('a', string='ISTAT').parent.next_sibling.getText()

            istat_code = istat_code.replace("\n", "").replace(" ", "")

        return City(city_link.get('title'), zip_code, region, istat_code)
