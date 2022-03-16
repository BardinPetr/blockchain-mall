from typing import Optional


from ariadne import ObjectType
import os

from auth.signatures import get_last_token, decode_token
from dto.authentication import Authentication

query = ObjectType("Query")


LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")


@query.field("authentication")
def resolve_request_authentication(_, info) -> Optional[Authentication]:
    cookies = info.context['request'].cookies
    print("IN resolve_request_authentication - cookies, last_user:", cookies)
    access_token = cookies.get('access_token_cookie')
    if access_token is None:
        return None

    access_token = decode_token(access_token)
    address = access_token['address']
    return Authentication(address, address == LANDLORD_ADDR)
