class InputRoom:
    internalName: str
    area: float
    location: str

    def __init__(self, internalName, area, location, id=None, contractAddress=None, publicName=None):
        self.internalName = internalName
        self.area = area
        self.location = location
        self.id = id
        self.contractAddress = contractAddress
        self.publicName = publicName
