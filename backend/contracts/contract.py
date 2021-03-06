import json
import os

from contracts.contract_wrapper import ContractWrapper
from dto.contractinfo import ContractInfo
from error.exceptions import ContractNotExistsError
from web3 import Web3

RPC_URL = os.getenv("RPC_URL", "https://sokol.poa.network")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

ABI = json.load(open('abi.json', 'r'))
ACCOUNT_PK = w3.eth.account.create().key.hex()


def initContract(address):
    return ContractWrapper(w3, w3.eth.gasPrice, ACCOUNT_PK, abi=ABI, address=address)


def getContractInfo(address) -> ContractInfo:
    print("IN getContractInfo - address: " + str(address))
    if address is None:
        raise ContractNotExistsError()

    print("IN getContractInfo - trying to initContract; address: " + str(address))
    contract = initContract(address)
    print("IN getContractInfo - trying to get contract properties; address: " + str(address) + " contract: " + str(
        contract))
    try:
        contractInfo = ContractInfo(
            address,
            contract.getLandlord(),
            contract.getTenant(),
            contract.getRentalRate(),
            contract.getBillingPeriodDuration(),
            contract.getBillingsCount(),
            contract.contractStatus()
        )
        print("IN getContractInfo - contractInfo: " + str(contractInfo))
        return contractInfo
    except BaseException as e:
        print("IN getContractInfo - can't get contractInfo, exception: ", e)
        raise e


def get_contract_cashiers(address):
    contract = initContract(address)
    return contract.getCashiersList()


def add_contract_cashier(contractAddress, cashier):
    contract = initContract(contractAddress)
    return contract.addCashier(cashier)


def get_contract_cashier_nonce(address, cashier_addr):
    contract = initContract(address)
    return contract.getCashierNonce(cashier_addr)


def does_contract_exists(address):
    try:
        address = w3.toChecksumAddress(address)
        # contract = ContractWrapper(w3, w3.eth.gasPrice, ACCOUNT_PK, abi=ABI, address=address)
        # print(w3.eth.getCode(address))
        if not w3.eth.getCode(address):
            return False
        # contract.getTenant()
    except BaseException as e:
        print("IN does_contract_exists - RPC_URL: ", str(RPC_URL))
        print("IN does_contract_exists - contract does not exists with address: " +
              str(address) + " exception: ", str(e))
        return False
    print("IN does_contract_exists - contract EXISTS with address: " + str(address))
    return True

# a = does_contract_exists("0x54b0eE7C64202e458BB90C54edf238e47E525413")
# print(a)
