from models.City import City


class MetropolitanCity(City):

    def get_zip_code(self, zip_code):

        zip_code = zip_code.replace("da", "")
        zip_code = zip_code.split("a")[0]
        zip_code = list(zip_code)
        zip_code[-1] = "0"
        zip_code = "".join(zip_code)

        return zip_code
