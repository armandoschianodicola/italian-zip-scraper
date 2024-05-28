from models.ItalianRegionCityFactory import ItalianRegionCityFactory


def create_factory(link):

    link = link.strip()
    
    return ItalianRegionCityFactory(link)
