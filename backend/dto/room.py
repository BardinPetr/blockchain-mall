class Room:
    id: str
    internalName: str
    area: float
    location: str
    contractAddress: str
    publicName: str

    def __init__(self, internalName, area, location, contractAddress=None, publicName=None, id=None):
        self.id = id
        self.internalName = internalName
        self.area = area
        self.location = location
        self.contractAddress = contractAddress
        self.publicName = publicName
