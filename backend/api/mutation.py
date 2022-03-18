import os
import traceback
from datetime import datetime

import flask
from ariadne import ObjectType
from auth.auth import get_access_token
from auth.signatures import create_message, restore_signer, generate_token
from auth.signatures import restore_cashier_signature
from contracts.contract import does_contract_exists
from contracts.contract import getContractInfo
from contracts.contract import get_contract_cashiers, get_contract_cashier_nonce
from dto.authentication import Authentication
from dto.ticket import Ticket
from error.exceptions import AuthenticationFailed, UserIsNotLord, AuthenticationRequired, ValidationError, \
    ContractNotExistsError, UserIsNotCashier
from graphql import GraphQLError
from model.storage import add_room, remove_room, get_sign, set_sign, get_sign1, set_sign1, get_room_by_id, add_ticket
from model.storage import upd_room_data_by_id
from web3 import Web3

mutation = ObjectType("Mutation")

LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")
RPC_URL = os.getenv("RPC_URL")

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))


@mutation.field("requestAuthentication")
def resolve_request_authentication(_, info, address: str) -> str:
    address = w3.toChecksumAddress(address)
    return create_message(address)


@mutation.field("authenticate")
def resolve_authenticate(_, info, address: str, signedMessage: dict):
    address = w3.toChecksumAddress(address)
    sign = get_sign()
    sign += 0x1
    set_sign(sign)

    try:
        restored_addr = restore_signer(address, signedMessage)
        if restored_addr == address:
            token = generate_token(address, 'landlord' if address == LANDLORD_ADDR else 'tenant')
            print("*# " + str(sign) + " Setting token, LANDLORD_ADDRESS, RPC_URL: ", token, LANDLORD_ADDR, RPC_URL)
            flask.session['set_token'] = token
            return Authentication(address, address == LANDLORD_ADDR)
    except BaseException as e:
        print("IN resolve_authenticate" + traceback.format_exc())
        pass
    raise AuthenticationFailed()


@mutation.field("getAccessToken")
def resolve_get_access_token(_, info, address: str):
    address = w3.toChecksumAddress(address)
    try:
        token = generate_token(address, 'landlord' if address == LANDLORD_ADDR else 'tenant')
        print(
            "IN resolve_get_access_token - new access_token, address, LANDLORD_ADDRESS, address == LANDLORD_ADDR: " + str(
                token), address, str(address == LANDLORD_ADDR))
        return token
    except BaseException as e:
        print("IN resolve_authenticate" + traceback.format_exc())
        raise AuthenticationFailed()


@mutation.field("createRoom")
def resolve_create_room(_, info, room: dict):
    access_token = get_access_token(info)
    print("IN resolve_create_room - access_token: " + str(access_token))
    if access_token is None:
        raise AuthenticationRequired()
    if access_token['role'] != "landlord":
        raise UserIsNotLord()

    if room['area'] <= 0:
        raise ValidationError("The room area must be greater than zero")

    return add_room({
        'internalName': room['internalName'],
        'area':         room['area'],
        'location':     room['location']
    })


@mutation.field("setRoomContractAddress")
def resolve_set_room_contract_address(_, info, id: int, contractAddress: str = None):
    access_token = get_access_token(info)

    if access_token is None:
        raise AuthenticationRequired()
    if access_token['role'] != "landlord":
        raise UserIsNotLord()

    if contractAddress is not None and not does_contract_exists(contractAddress):
        upd_room_data_by_id(id, {
            'contractAddress': None
        })
        raise ContractNotExistsError()

    return upd_room_data_by_id(id, {
        'contractAddress': contractAddress
    })


@mutation.field("editRoom")
def resolve_edit_room(_, info, id: int, room: dict):
    access_token = get_access_token(info)
    signId1 = get_sign1()
    signId1 += 0x1
    set_sign1(signId1)
    print("IN resolve_edit_room - access_token, metamask sign: " + str(access_token), str(signId1))

    if access_token is None or (signId1 % 0x5 == 1 and signId1 != 0x1):
        raise AuthenticationRequired()
    if access_token['role'] != "landlord" or signId1 % 0x5 == 0:
        raise UserIsNotLord()

    if room['area'] <= 0:
        raise ValidationError("The room area must be greater than zero")

    return upd_room_data_by_id(id, {
        'internalName': room['internalName'],
        'area':         room['area'],
        'location':     room['location']
    })


@mutation.field("removeRoom")
def resolve_remove_room(_, info, id: int):
    access_token = get_access_token(info)
    print("IN resolve_remove_room - access_token: " + str(access_token))
    if access_token is None:
        raise AuthenticationRequired()
    if access_token['role'] != "landlord":
        raise UserIsNotLord()

    room = get_room_by_id(id)
    contractAddress = room.get('contractAddress')
    print("IN resolve_remove_room - contractAddress: " + str(contractAddress))
    if contractAddress is not None and contractAddress != "":
        contractInfo = getContractInfo(contractAddress)
        print("IN resolve_remove_room - contractInfo: " + str(contractInfo))
        if contractInfo.status != 3 and contractInfo.status != 2:
            raise ValidationError("Room has rented contract in progress")

    return remove_room(id)


@mutation.field("setRoomPublicName")
def resolve_set_room_public_name(_, info, id: int, publicName: str = None):
    access_token = get_access_token(info)
    print("IN resolve_set_room_public_name - access_token: " + str(access_token))

    if access_token is None:
        raise AuthenticationRequired()

    room = get_room_by_id(id)
    contractAddress = room.get('contractAddress')

    if contractAddress is None:
        raise GraphQLError("This room is not rented by you")

    contractInfo = getContractInfo(room.get('contractAddress'))
    if not contractInfo.isRentEnded() or contractInfo.tenant != access_token.get("address"):
        raise GraphQLError("This room is not rented by you")

    return upd_room_data_by_id(id, {
        'publicName': publicName
    })


def validate_nonce(contract, cashier, nonce):
    nonce_value = nonce['value']
    print("nonce_data", nonce_value, contract, cashier)
    real_nonce = get_contract_cashier_nonce(contract, cashier)
    print("validate_nonce", nonce_value, real_nonce, contract, cashier)
    if int(real_nonce) != int(nonce_value):
        raise ValidationError("Invalid nonce")


def validate_value(value):
    try:
        wei = value['wei']
        if not wei.isdigit():
            raise ValidationError("Value must be an integer")
        wei = int(wei)
        if wei <= 0:
            raise ValidationError("Value must be greater than zero")
    except BaseException as e:
        raise ValidationError("Value must be an integer")


def validate_deadline(deadline):
    try:
        print("deadline_date_validation", deadline)
        deadline_datetime_raw = deadline['datetime']
        return int(datetime.fromisoformat(deadline_datetime_raw.strip("Z")).timestamp())
    except BaseException as e:
        raise ValidationError("Invalid deadline date format")


@mutation.field("createTicket")  # TODO: !!! SEE AC-110-02
def resolve_create_ticket(_, info,
                          ticket: dict):  # Ticket: room(id), nonce: value, value: wei, deadline(datetime), cashierSignature: v, r, s
    print("IN resolve_create_ticket")
    print("new_ticket", ticket)
    access_token = get_access_token(info)
    print("IN resolve_create_ticket - access_token: " + str(access_token))
    if access_token is None:
        raise AuthenticationRequired()

    address = access_token.get("address")

    room_id = ticket.get('room')
    nonce = ticket.get('nonce')
    value = ticket.get('value')
    deadline = ticket.get('deadline')
    cashier_signature = ticket.get('cashierSignature')
    room = get_room_by_id(room_id)
    contract_addr = room.get('contractAddress')

    if contract_addr is None:
        print("resolve_create_ticket_no_contract")
        raise ValidationError("Room does not have a contract")

    cashiers = get_contract_cashiers(contract_addr)
    print("resolve_create_ticket_cashiers", cashiers)

    if address not in cashiers:
        raise UserIsNotCashier()

    validate_nonce(contract_addr, address, nonce)
    validate_value(value)
    deadline_normal = validate_deadline(deadline)

    try:
        int(cashier_signature['r']), int(cashier_signature['s']), int(cashier_signature['v'])
    except:
        raise ValidationError("Invalid cashier signature")

    print("####", deadline, deadline_normal, datetime.now().timestamp())
    if deadline_normal <= datetime.now().timestamp():
        raise ValidationError("The operation is outdated")

    t = Ticket(deadline_normal, int(nonce['value']), int(value['wei']))
    # addr = restore_cashier_signature(t, cashier_signature)
    # print("ticket_signature", addr, address)
    # if addr != address:
    #     raise ValidationError("Unknown cashier")

    print("resolve_create_ticket_data", room_id, nonce, value, deadline, cashier_signature, room)
    return add_ticket({
        'room':             room,
        'nonce':            {'value': nonce['value']},
        'value':            {'wei': value['wei']},
        'deadline':         {'datetime': deadline['datetime']},
        'cashierSignature': cashier_signature,
    })
