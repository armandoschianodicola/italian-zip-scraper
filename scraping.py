from bs4 import BeautifulSoup
import requests
import re
import time
import csv
import os

my_file = open("cities.txt", "r")

# reading the file
data = my_file.read()

# replacing end of line('/n') with ' ' and
# splitting the text it further when '.' is seen.
regions_list = data.replace('\n', ' ').split(".")

# printing the data
print(regions_list)
my_file.close()

try:

    # field names
    fields = [
        'name',
        # 'istat_code',
        'zip'
    ]

    # name of csv file
    filename = "italian_cities.csv"

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

        time.sleep(3)

        for city_link in list(cities_links):
            print(city_link.get('href'))

            city = requests.get("https://it.wikipedia.org/{}".format(city_link.get('href')))

            city_soup = BeautifulSoup(city.content, 'html.parser')

            print(city_soup)

            info_table = city_soup.find('table', {"class": "infobox sinottico"})

            if info_table is not None:

                zip_code = info_table.find('th', string='Cod. postale').next_sibling.getText()

                zip_code = zip_code.replace("\n", "").replace(" ", "")

                # istat_code = info_table.find('th', string=re.compile(r'Codice*')).next_sibling.getText()
                #
                # istat_code = istat_code.replace("\n", "").replace(" ", "")

                city_data = {
                    'name': city_link.text,
                    # 'istat_code': istat_code,
                    'zip': zip_code
                }

                with open(filename, 'w') as csvfile:
                    # creating a csv dict writer object
                    writer = csv.DictWriter(csvfile, fieldnames=fields)

                    # writing headers (field names)

                    if not os.path.isfile(filename):
                        writer.writeheader()

                    # writing data rows
                    writer.writerow(city_data)

            print(city_soup)

        print(cities_links)
        print(len(cities_links))

except Exception as e:
    print(e)
    print("Error")
