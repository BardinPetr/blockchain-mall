class Authentication:
    address: str
    isLandlord: bool
    token: str

    def __init__(self, address, is_landlord, token):
        self.address = address
        self.isLandlord = is_landlord
        self.token = token
