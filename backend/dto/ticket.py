from eip712_structs import EIP712Struct, Uint


class Ticket(EIP712Struct):
    deadline = Uint(256)
    nonce = Uint(256)
    value = Uint(256)
