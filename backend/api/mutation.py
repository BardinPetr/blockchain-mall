import os
import time
import traceback


from ariadne import ObjectType
from dto.authentication import Authentication
from dto.input_room import InputRoom
from dto.room import Room
from web3 import Web3

from error.exceptions import AuthenticationFailed, UserIsNotLord, AuthenticationRequired, ValidationError
from auth.signatures import create_message, restore_signer, generate_token, set_last_token

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
            token = generate_token(address, 'landlord' if address == LANDLORD_ADDR else 'user')
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
        return generate_token(address, 'landlord' if address == LANDLORD_ADDR else 'user')
    except BaseException as e:
        print("IN resolve_authenticate" + traceback.format_exc())
        raise resolve_get_access_token()


@mutation.field("createRoom")
def resolve_create_room(_, info, room: InputRoom):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    print("IN resolve_create_room - cookies, access_token: ", cookies, access_token)
    if access_token is None:
        raise AuthenticationRequired()

    if room.area <= 0:
        raise ValidationError("The room area must be greater than zero")


@mutation.field("setRoomContractAddress")
def resolve_set_room_contract_address(_, info, id: int, address: str):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    print("IN resolve_set_room_contract_address - cookies, access_token: ", cookies, access_token)
    if access_token is None:
        raise AuthenticationRequired()


@mutation.field("editRoom")
def resolve_edit_room(_, info, id: int, room: InputRoom):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    print("IN resolve_edit_room - cookies, access_token: ", cookies, access_token)
    if access_token is None:
        raise AuthenticationRequired()


@mutation.field("removeRoom")
def resolve_remove_room(_, info, id: int):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    print("IN resolve_remove_room - cookies, access_token: ", cookies, access_token)
    if access_token is None:
        raise AuthenticationRequired()


@mutation.field("setRoomPublicName")
def resolve_set_room_public_name(_, info, id: int, publicName: str):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    print("IN resolve_set_room_public_name - cookies, access_token: ", cookies, access_token)
    if access_token is None:
        raise AuthenticationRequired()
