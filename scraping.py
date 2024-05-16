from bs4 import BeautifulSoup
import requests
import re

my_file = open("cities.txt", "r")

# reading the file
data = my_file.read()

# replacing end of line('/n') with ' ' and
# splitting the text it further when '.' is seen.
regions_list = data.replace('\n', ' ').split(".")

# printing the data
print(regions_list)
my_file.close()

for i, region_text_link in enumerate(regions_list, start=1):

    print("---------------------------------------------------")
    print("Region: ", i)

    # get URL
    page = requests.get("https://it.wikipedia.org/wiki/{}".format(region_text_link))

    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')

    cities_table = soup.find('table')

    cities_links = cities_table.find_all('a', href=re.compile(r'/wiki/.*'))

    cities_links = filter(lambda x: "Provincia_" not in x.get('href'), cities_links)

    for city_link in list(cities_links):
        print(city_link.get('href'))

        city = requests.get("https://it.wikipedia.org/{}".format(city_link.get('href')))

        city_soup = BeautifulSoup(city.content, 'html.parser')

        print(city_soup)

        info_table = city_soup.find('table', {"class": "infobox sinottico"})

        if info_table is not None:

            zip_code = info_table.find('th', text='Cod. postale').next_sibling.text

            zip_code = zip_code.replace("\n", "").replace(" ", "")

        print(city_soup)

    print(cities_links)
    print(len(cities_links))
