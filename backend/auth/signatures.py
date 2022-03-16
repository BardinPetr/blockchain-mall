import os
from time import time_ns

import dotenv
import eth_account
import jwt
from eip712_structs import make_domain
from web3 import Web3

from auth.msgs import AuthMsg

dotenv.load_dotenv(verbose=True, override=True)
LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")
JWTKEY = os.getenv("JWT_KEY", "testkey")

domain = make_domain(name='Rental Agreement', version='1.0')

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
store = {}
last_user = {}


def create_message(address):
    global store
    msg = address + "@" + str(time_ns())
    store[address] = msg
    return msg


def restore_signer(address, signature):
    print("IN restore_signer address, signature, store: ", address, signature, store)
    msg = eth_account.messages.encode_defunct(store[address].encode('utf-8'))
    return w3.eth.account.recover_message(msg, vrs=(int(signature['v'], 16), signature['r'], signature['s']))


def generate_token(address, role):
    return jwt.encode({"address": address, "role": role},
                      JWTKEY,
                      algorithm="HS256")


def decode_token(token):
    try:
        return jwt.decode(token, JWTKEY, algorithms="HS256")
    except:
        return None


def set_last_user(_last_user):
    global last_user
    last_user = _last_user


def get_last_user():
    global last_user
    return last_user
