import os
import time
import traceback
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
    try:
        contractInfo = getContractInfo(room.get('contractAddress'))
        room['landlord'] = contractInfo.landlord
        room['tenant'] = contractInfo.tenant
        room['rentalRate'] = contractInfo.rentalRate
        room['billingPeriodDuration'] = contractInfo.billingPeriodDuration
        room['billingsCount'] = contractInfo.billingsCount
        room['status'] = contractInfo.status
    except BaseException as e:
        print("IN resolve_get_room - exception during getContractInfo; room: " + str(room) + " exception: " + str(e))
        print(traceback.format_exc())
        room['status'] = 0
        return room

    return room


@query.field("rooms")
def resolve_get_rooms(_, info):
    access_token = get_access_token(info)
    if access_token is None:
        raise AuthenticationRequired()

    rooms = get_rooms()
    print("IN resolve_get_rooms - rooms: " + str(rooms))
    if access_token['role'] == "landlord":
        return rooms

    currentAddress = access_token.get('tenantAddress')
    rooms = list(rooms)

    tenant_rooms = []
    not_tenant_rooms = []
    for room in rooms:
        contractAddress = room.get('contractAddress')
        if contractAddress is None or contractAddress == "":
            continue

        contractInfo = getContractInfo(room.get('contractAddress'))
        print("IN resolve_get_rooms - contractInfo: " + str(contractInfo) + " tenantAddress: " + str(currentAddress) + " contractInfo.isRentEnded: " + str(contractInfo.isRentEnded()))
        if not contractInfo.isReadyForRent()
            if contractInfo.tenant == currentAddress:
                tenant_rooms.append(room)
            else:
                not_tenant_rooms.append(room)

    print("IN resolve_get_rooms - tenant_rooms: " + str(tenant_rooms) + " not_tenant_rooms: " + str(not_tenant_rooms))
    if len(tenant_rooms) == 0:
        return not_tenant_rooms
    else:
        return tenant_rooms

    # rooms_if_tenant = []
    # rooms_if_not_tenant = []
    # for room in rooms:
    #     contractAddress = room.get('contractAddress')
    #     if contractAddress is None or contractAddress == "":
    #         continue
    #
    #     contractInfo = getContractInfo(room.get('contractAddress'))
    #     print("IN resolve_get_rooms - contractInfo: " + str(contractInfo) + " tenantAddress: " + str(tenantAddress) + " contractInfo.isRentEnded: " + str(contractInfo.isRentEnded()))
    #     if not contractInfo.isRentEnded():
    #         if contractAddress is None or contractInfo.tenant != tenantAddress:
    #             rooms_if_not_tenant.append(room)
    #         else:
    #             rooms_if_tenant.append(room)
    #
    # print("IN resolve_get_rooms - rooms_if_tenant: " + str(rooms_if_tenant) + " rooms_if_not_tenant: " + str(rooms_if_not_tenant))
    # if len(rooms_if_tenant) != 0:
    #     return rooms_if_tenant
    # else:
    #     return rooms_if_not_tenant


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
