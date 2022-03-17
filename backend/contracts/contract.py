import json
import traceback

from web3 import Web3
import os


from backend.dto.contractinfo import ContractInfo
from contracts.contract_wrapper import ContractWrapper
from error.exceptions import ContractNotExistsError

RPC_URL = os.getenv("RPC_URL", "https://sokol.poa.network")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

ABI = json.load(open('abi.json', 'r'))
ACCOUNT_PK = w3.eth.account.create().key.hex()


def initContract(address):
    return ContractWrapper(w3, w3.eth.gasPrice, ACCOUNT_PK, abi=ABI, address=address)


def getContractInfo(address) -> ContractInfo:
    if address is None:
        raise ContractNotExistsError()

    contract = initContract(address)
    return ContractInfo(
        address,
        contract.getLandlord(),
        contract.getTenant(),
        contract.getRentalRate(),
        contract.getBillingPeriodDuration(),
        contract.getBillingsCount(),
        contract.getStatus()
    )


def does_contract_exists(address):
    try:
        address = w3.toChecksumAddress(address)
        contract = ContractWrapper(w3, w3.eth.gasPrice, ACCOUNT_PK, abi=ABI, address=address)
        contract.getTenant()
        w3.eth.getCode(address)
    except BaseException as e:
        print("IN does_contract_exists - RPC_URL: ", str(RPC_URL))
        print("IN does_contract_exists - contract does not exists with address: " +
              str(address) + " exception: ", str(e))
        return False
    print("IN does_contract_exists - contract EXISTS with address: " + str(address))
    return True

# a = getContractInfo('123', "0x54b0eE7C64202e458BB99C54edf238e47E525413")
# print(a)
