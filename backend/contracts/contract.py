import json

from web3 import Web3
import os

from contracts.contract_wrapper import ContractWrapper

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL", "https://sokol.poa.network")))

ABI = json.load(open('abi.json', 'r'))
ACCOUNT_PK = w3.eth.account.create().key.hex()


def getContractData(address):
    contract = ContractWrapper(w3, w3.eth.gasPrice, ACCOUNT_PK, abi=ABI, address=address)
    return contract.getTenant()


def does_contract_exists(address):
    try:
        contract = ContractWrapper(w3, w3.eth.gasPrice, ACCOUNT_PK, abi=ABI, address=address)
        contract.getTenant()
    except Exception as e:
        return False
    return True


# print(getContractData("0x9d039286e87dA118858f00CB6B15abE8A4C1Fc7e"))
