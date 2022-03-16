class Room:
    id: int
    internalName: str
    area: float
    location: str
    contractAddress: str
    publicName: str

    def __init__(self, id, internalName, area, location, contractAddress, publicName):
        self.id = id
        self.internalName = internalName
        self.area = area
        self.location = location
        self.contractAddress = contractAddress
        self.publicName = publicName
