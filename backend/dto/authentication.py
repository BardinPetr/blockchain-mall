class Authentication:
    address: str
    isLandlord: bool

    def __init__(self, address, is_landlord):
        self.address = address
        self.isLandlord = is_landlord
