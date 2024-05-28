import time
import csv
import os

from utils.factory import create_factory

my_file = open("regions.txt", "r")

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

    cities_data_in = []
    cities_data_out = []

    if not os.path.exists(filename):
        with open(filename, 'w') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            # writing headers (field names)
            writer.writeheader()

    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader, None)
        cities_data_in = [row[1] for row in reader]

    for i, region_text_link in enumerate(regions_list, start=1):

        print("---------------------------------------------------")
        print("Region: ", i, 'of', len(regions_list))

        region_factory = create_factory(region_text_link)

        city_links = region_factory.create_city_list()

        time.sleep(2)

        for j, city_link in enumerate(city_links, start=1):

            print("City: ", j, 'of', len(city_links))

            if city_link.get('title') not in cities_data_in:

                time.sleep(2)

                city = region_factory.create_city(city_link)
                print("City: ", city)

                city_index = city.get_index()

                if city_index is not None and city_index not in cities_data_in:

                    city_data = {
                        'name': city.name,
                        'zip': city.zip,
                        'region': city.region,
                        "istat_code": city.istat_code,
                    }
                    cities_data_out.append(city_data)

    if cities_data_out:
        with open(filename, 'a') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            # writing data rows
            writer.writerows([
                {
                    'istat_code': c.get('istat_code'),
                    'name': c.get('name'),
                    'zip': c.get('zip'),
                    'region': c.get('region'),
                } for c in cities_data_out
            ])


except Exception as e:
    print(e)
    print("Error")
