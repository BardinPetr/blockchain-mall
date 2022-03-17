import os
import time
from typing import Optional

from ariadne import ObjectType

from auth.auth import get_access_token
from dto.authentication import Authentication
from dto.contractinfo import ContractInfo
from error.exceptions import AuthenticationRequired, UserIsNotLord
from model.storage import get_room_by_id, get_rooms

from contracts.contract import getContractInfo

query = ObjectType("Query")

LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")


@query.field("authentication")
def resolve_request_authentication(_, info) -> Optional[Authentication]:
    access_token = get_access_token(info)
    if access_token is None:
        return None

    address = access_token['address']
    return Authentication(address, address == LANDLORD_ADDR)


@query.field("room")
def resolve_get_room(_, info, id: int):
    access_token = get_access_token(info)
    if access_token is None:
        raise AuthenticationRequired()

    room = get_room_by_id(id)
    if room.get('isAvailableForRent') is None:
        room['isAvailableForRent'] = False
    if room.get('status') is None:
        room['status'] = int(time.time())
    if room.get('tenant') is None:
        room['tenant'] = "0xCB0A9b2978d26C1233324a424910B7Db892dB62C"
    if room.get('rentStart') is None:
        room['rentStart'] = int(time.time())
    if room.get('rentEnd') is None:
        room['rentEnd'] = int(time.time())
    if room.get('billingPeriod') is None:
        room['billingPeriod'] = int(time.time() - 9999)
    if room.get('rentalRate') is None:
        room['rentalRate'] = 666

    return room


@query.field("rooms")
def resolve_get_rooms(_, info):
    access_token = get_access_token(info)
    if access_token is None:
        raise AuthenticationRequired()
    if access_token['role'] != "landlord":
        raise UserIsNotLord()

    return get_rooms()


@query.field("getContractInfo")
def resolve_get_contract(_, info, id: int) -> ContractInfo:
    access_token = get_access_token(info)
    if access_token is None:
        raise AuthenticationRequired()

    addr = get_room_by_id(id)['contractAddress']
    return getContractInfo(id, addr)

