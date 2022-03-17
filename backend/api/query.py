import os
from typing import Optional

from ariadne import ObjectType

from auth.auth import get_access_token
from dto.authentication import Authentication
from error.exceptions import AuthenticationRequired, UserIsNotLord
from model.storage import get_room_by_id, get_rooms

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
    if access_token['role'] != "landlord":
        raise UserIsNotLord()

    return get_room_by_id(id)


@query.field("rooms")
def resolve_get_rooms(_, info, id: int):
    access_token = get_access_token(info)
    if access_token is None:
        raise AuthenticationRequired()
    if access_token['role'] != "landlord":
        raise UserIsNotLord()

    return get_rooms()
