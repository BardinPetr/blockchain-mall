import os
import time
import traceback


from ariadne import ObjectType

from auth.auth import get_access_token
from dto.authentication import Authentication
from dto.input_room import InputRoom
from dto.room import Room
from web3 import Web3

from error.exceptions import AuthenticationFailed, UserIsNotLord, AuthenticationRequired, ValidationError, \
    RoomNotFoundError
from auth.signatures import create_message, restore_signer, generate_token, set_last_token
from model.storage import add_room

from auth.signatures import decode_token

from model.storage import upd_room_data_by_id

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

    try:
        restored_addr = restore_signer(address, signedMessage)
        if restored_addr == address:
            token = generate_token(address, 'landlord' if address == LANDLORD_ADDR else 'tenant')
            print("Setting token, LANDLORD_ADDRESS, RPC_URL: ", token, LANDLORD_ADDR, RPC_URL)
            set_last_token(token)
            return Authentication(address, address == LANDLORD_ADDR)
    except BaseException as e:
        print("IN resolve_authenticate" + traceback.format_exc())
        pass
    raise AuthenticationFailed()


@mutation.field("getAccessToken")
def resolve_get_access_token(_, info, address: str):
    address = w3.toChecksumAddress(address)
    try:
        return generate_token(address, 'landlord' if address == LANDLORD_ADDR else 'tenant')
    except BaseException as e:
        print("IN resolve_authenticate" + traceback.format_exc())
        raise resolve_get_access_token()


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
        'area': room['area'],
        'location': room['location']
    })


@mutation.field("setRoomContractAddress")
def resolve_set_room_contract_address(_, info, id: int, contractAddress: str = None):
    access_token = get_access_token(info)
    print("IN resolve_set_room_contract_address - access_token, headers: ", access_token, info.context['request'].headers)
    if access_token is None:
        raise AuthenticationRequired()
    if access_token['role'] != "landlord":
        raise UserIsNotLord()

    return upd_room_data_by_id(id, {
        'contractAddress': contractAddress
    })


@mutation.field("editRoom")
def resolve_edit_room(_, info, id: int, room: dict):
    access_token = get_access_token(info)
    print("IN resolve_edit_room - access_token: " + str(access_token))
    if access_token is None:
        raise AuthenticationRequired()
    if access_token['role'] != "landlord":
        raise UserIsNotLord()

    if room['area'] <= 0:
        raise ValidationError("The room area must be greater than zero")

    return upd_room_data_by_id(id, {
       'internalName': room['internalName'],
       'area': room['area'],
       'location': room['location']
    })


@mutation.field("removeRoom")
def resolve_remove_room(_, info, id: int):
    access_token = get_access_token(info)
    print("IN resolve_remove_room - access_token: " + str(access_token))
    if access_token is None:
        raise AuthenticationRequired()
    if access_token['role'] != "landlord":
        raise UserIsNotLord()


@mutation.field("setRoomPublicName")
def resolve_set_room_public_name(_, info, id: int, publicName: str = None):
    access_token = get_access_token(info)
    print("IN resolve_set_room_public_name - access_token: " + str(access_token))

    if access_token is None:
        raise AuthenticationRequired()

    return upd_room_data_by_id(id, {
        'publicName': publicName
    })
