class ContractInfo:
    contractAddress: str
    landlord: str
    tenant: str
    rentalRate: int
    billingPeriodDuration: int
    billingsCount: int
    status: int

    def __init__(self,
                 contractAddress: str,
                 landlord: str,
                 tenant: str,
                 rentalRate: int,
                 billingPeriodDuration: int,
                 billingsCount: int,
                 status: int):
        self.contractAddress = contractAddress
        self.landlord = landlord
        self.tenant = tenant
        self.rentalRate = rentalRate
        self.billingPeriodDuration = billingPeriodDuration
        self.billingsCount = billingsCount
        self.status = status

    def isRentEnded(self):
        return self.status == 3
