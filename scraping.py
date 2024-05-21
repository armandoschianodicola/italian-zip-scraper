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
    headers = [
        'istat_code',
        'name',
        'zip',
        'region',
    ]

    # name of csv file
    filename = "italian_cities.csv"

    cities_data_in = {}
    cities_data_out = {}

    if not os.path.exists(filename):
        with open(filename, 'w') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            # writing headers (field names)
            writer.writeheader()

    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader, None)
        cities_data_in = {row[0]: {'name': row[1], 'zip': row[2], 'region': row[3]} for row in reader}

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
        cities_links_list = list(cities_links)
        print("Cities: ", len(cities_links_list))

        time.sleep(2)

        for city_link in cities_links_list:
            print(city_link.get('href'))

            time.sleep(2)

            city = requests.get("https://it.wikipedia.org/{}".format(city_link.get('href')))

            city_soup = BeautifulSoup(city.content, 'html.parser')

            info_table = city_soup.find('table', {"class": "infobox sinottico"})

            if info_table is not None:

                region = info_table.find('th', string='Regione').next_sibling.getText()

                region = region.replace("\n", "").replace(" ", "")

                zip_code = info_table.find('th', string='Cod. postale').next_sibling.getText()

                zip_code = zip_code.replace("\n", "").replace(" ", "")

                istat_code = info_table.find('a', string='ISTAT').parent.next_sibling.getText()

                istat_code = istat_code.replace("\n", "").replace(" ", "")

                if istat_code not in cities_data_in:

                    city_data = {
                        'name': city_link.text,
                        'zip': zip_code,
                        'region': region
                    }
                    cities_data_out[istat_code] = city_data

    if cities_data_out:
        with open(filename, 'a') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            # writing data rows
            writer.writerows([
                {
                    'istat_code': key,
                    'name': value['name'],
                    'zip': value['zip'],
                    'region': value['region']
                } for key, value in cities_data_out.items()
            ])


except Exception as e:
    print(e)
    print("Error")
