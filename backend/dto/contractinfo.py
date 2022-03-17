class ContractInfo:
    id: int
    contractAddress: str
    landlord: str
    tenant: str
    rentalRate: int
    billingPeriodDuration: int
    billingsCount: int

    def __init__(self, id: int,
                 contractAddress: str,
                 landlord: str,
                 tenant: str,
                 rentalRate: int,
                 billingPeriodDuration: int,
                 billingsCount: int):
        self.id = id
        self.contractAddress = contractAddress
        self.landlord = landlord
        self.tenant = tenant
        self.rentalRate = rentalRate
        self.billingPeriodDuration = billingPeriodDuration
        self.billingsCount = billingsCount
