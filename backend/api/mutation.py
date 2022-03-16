import os
import time
import traceback

import dotenv
from ariadne import ObjectType
from dto.authentication import Authentication
from dto.input_room import InputRoom
from dto.room import Room

from error.exceptions import AuthenticationFailed, UserIsNotLord, AuthenticationRequired, ValidationError
from auth.signatures import create_message, restore_signer, generate_token

mutation = ObjectType("Mutation")

dotenv.load_dotenv(verbose=True, override=True)
LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")


@mutation.field("requestAuthentication")
def resolve_request_authentication(_, info, address: str) -> str:
    return create_message(address)


@mutation.field("authenticate")
def resolve_authenticate(_, info, address: str, signedMessage: dict):
    try:
        address = address
        restored_addr = restore_signer(address, signedMessage)
        if restored_addr == address:
            return Authentication(address, address == LANDLORD_ADDR)
    except BaseException as e:
        print("IN resolve_authenticate" + traceback.format_exc())
        pass
    raise AuthenticationFailed()

#        bipki
@mutation.field("getAccessToken")
def resolve_get_access_token(_, info, address: str, signedMessage: dict):
    try:
        return generate_token(address, 'landlord' if address == LANDLORD_ADDR else 'user')
    except BaseException as e:
        print("IN resolve_authenticate" + traceback.format_exc())
        raise resolve_get_access_token()

@mutation.field("createRoom")
def resolve_create_room(_, info, room: InputRoom):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    if access_token is None:
        raise AuthenticationRequired()

    if room.area <= 0:
        raise ValidationError("The room area must be greater than zero")


@mutation.field("setRoomContractAddress")
def resolve_set_room_contract_address(_, info, id: int, address: str):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    if access_token is None:
        raise AuthenticationRequired()


@mutation.field("editRoom")
def resolve_edit_room(_, info, id: int, room: InputRoom):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    if access_token is None:
        raise AuthenticationRequired()


@mutation.field("removeRoom")
def resolve_remove_room(_, info, id: int):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    if access_token is None:
        raise AuthenticationRequired()


@mutation.field("setRoomPublicName")
def resolve_remove_room(_, info, id: int, publicName: str):
    cookies = info.context['request'].cookies
    access_token = cookies.get("access_token_cookie")
    if access_token is None:
        raise AuthenticationRequired()
