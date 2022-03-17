import eth_account
from web3 import Web3, HTTPProvider
import dotenv
import os
from eip712_structs import make_domain, EIP712Struct, Boolean, Uint, Address

from backend.web3.msgs import AuthMsg

dotenv.load_dotenv(verbose=True, override=True)
LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")

domain = make_domain(name='Rental Agreement', version='1.0')

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
store = {}


def create_message(address):
    global store
    msg = AuthMsg(address=address, is_landlord=(address == LANDLORD_ADDR))
    msg_json = msg.to_message_json(domain)
    store[address] = msg_json
    return msg_json


def restore_signer(address, signature):
    msg = eth_account.messages.encode_structured_data(text=store[address])
    return w3.eth.account.recover_message(msg, vrs=(int(signature['v']), signature['r'], signature['s']))
