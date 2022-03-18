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

    def isReadyForRent(self):
        return self.status == 2 or self.status == 3

    def __str__(self) -> str:
        return "ContractInfo(contractAddress=" + str(self.contractAddress) + "," \
                                                                             "landlord=" + str(self.landlord) + "," \
                                                                                                                "tenant=" + str(
            self.tenant) + "," \
                           "rentalRate=" + str(self.rentalRate) + "," \
                                                                  "billingPeriodDuration=" + str(
            self.billingPeriodDuration) + "," \
                                          "billingsCount=" + str(self.billingsCount) + "," \
                                                                                       "status=" + str(
            self.status) + ")"
