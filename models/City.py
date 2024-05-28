
class City:
    def __init__(self, name, zip_code, region, istat_code):
        self.name = name
        self.zip = zip_code
        self.region = region
        self.istat_code = istat_code

    def __str__(self):
        return "City: {} - Zip: {} - Region: {} - Istat: {}".format(
            self.name,
            self.zip,
            self.region,
            self.istat_code
        )

    def get_index(self):
        return self.name
