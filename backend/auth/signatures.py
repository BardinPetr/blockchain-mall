import os
from time import time_ns

import eth_account
import jwt
from eip712_structs import make_domain
from web3 import Web3

from dto.ticket import Ticket
from error.exceptions import ValidationError

LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")
JWTKEY = os.getenv("JWT_KEY", "testkey")

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
store = {}
last_token = None


def create_message(address):
    global store
    msg = address + "@" + str(time_ns())
    store[address] = msg
    return msg


def restore_signer(address, signature):
    print("IN restore_signer address, signature, store: ", address, signature, store)
    msg = eth_account.messages.encode_defunct(store[address].encode('utf-8'))
    signer = w3.eth.account.recover_message(msg, vrs=(int(signature['v'], 16), signature['r'], signature['s']))
    del store[address]
    return signer


def restore_cashier_signature(ticket: Ticket, signature, contract):
    try:
        domain = make_domain(name='Rental Agreement', version='1.0', verifyingContract=contract)
        msg = ticket.to_message_json(domain)
        msg = eth_account.messages.encode_structured_data(text=msg)
        return w3.eth.account.recover_message(msg, vrs=(int(signature['v'], 16), signature['r'], signature['s']))
    except BaseException as e:
        raise ValidationError("Unknown cashier")


def generate_token(address, role):
    return jwt.encode({"address": address, "role": role},
                      JWTKEY,
                      algorithm="HS256")


def decode_token(token):
    try:
        return jwt.decode(token, JWTKEY, algorithms="HS256")
    except:
        return None


def set_last_token(_last_user):
    global last_token
    last_token = _last_user


def get_last_token():
    global last_token
    return last_token


def clear_last_token():
    global last_token
    last_token = None
