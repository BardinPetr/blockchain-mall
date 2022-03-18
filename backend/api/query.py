import os
import time
from typing import Optional

from ariadne import ObjectType

from auth.auth import get_access_token
from dto.authentication import Authentication
from dto.contractinfo import ContractInfo
from error.exceptions import AuthenticationRequired, UserIsNotLord
from model.storage import get_room_by_id, get_rooms, get_ticket_by_id

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
    return room


@query.field("rooms")
def resolve_get_rooms(_, info):
    access_token = get_access_token(info)
    if access_token is None:
        raise AuthenticationRequired()

    if access_token['role'] == "landlord":
        return get_rooms()

    tenantAddress = access_token.get('tenantAddress')
    rooms = list(get_rooms())
    rooms_if_tenant = []
    rooms_if_not_tenant = []
    for room in rooms:
        contractAddress = room.get('contractAddress')
        if contractAddress is None or contractAddress == "":
            rooms_if_not_tenant.append(room)
            continue

        contractInfo = getContractInfo(room.get('contractAddress'))
        if not contractInfo.isRentEnded():
            if contractAddress is None or contractInfo.tenant != tenantAddress:
                rooms_if_not_tenant.append(room)
            else:
                rooms_if_tenant.append(room)

    if len(rooms_if_tenant) != 0:
        return rooms_if_tenant
    else:
        return rooms_if_not_tenant


@query.field("getContractInfo")
def resolve_get_contract(_, info, id: int) -> ContractInfo:
    access_token = get_access_token(info)
    if access_token is None:
        raise AuthenticationRequired()

    addr = get_room_by_id(id)['contractAddress']
    return getContractInfo(id, addr)


@query.field("ticket")
def resolve_get_ticket(_, info, id: int):
    return get_ticket_by_id(id)


@query.field("getRpcUrl")
def resolve_rpc_url(_, info):
    return os.getenv("RPC_URL")
