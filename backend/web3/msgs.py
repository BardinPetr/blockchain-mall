import time

from eip712_structs import EIP712Struct, Boolean, Uint, Address


class AuthMsg(EIP712Struct):
    address = Address()
    is_landlord = Boolean()
    timestamp = Uint(256)

    def __init__(self, **kwargs):
        super().__init__(timestamp=int(time.time()), **kwargs)
