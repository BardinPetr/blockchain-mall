from typing import Optional

from ariadne import ObjectType
import os

from auth.signatures import get_last_token, decode_token
from dto.authentication import Authentication
from error.exceptions import AuthenticationRequired
from model.storage import get_room_by_id

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

    return get_room_by_id(id)


def get_access_token(info):
    cookies = info.context['request'].cookies
    print("IN get_access_token - cookies:", cookies)
    access_token = cookies.get('access_token_cookie')
    if access_token is None:
        access_token = info.context['request'].headers.get('CookiePlayground')
        if access_token is None:
            return None
        access_token = access_token.split("=")[1]
    return decode_token(access_token)
