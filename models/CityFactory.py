
from abc import ABC, abstractmethod


class CityFactory(ABC):

    def __init__(self, link):
        self.link = link

    @abstractmethod
    def create_city_list(self):

        pass

    @abstractmethod
    def create_city(self):

        pass
