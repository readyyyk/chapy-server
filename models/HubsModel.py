from typing import Dict
from models.HubModel import HubModel


class HubsModel:
    hubs: Dict[str, HubModel]

    def __init__(self):
        self.hubs = dict[str, HubModel]()

    def names(self):
        return self.hubs.keys()


hubs = HubsModel()
