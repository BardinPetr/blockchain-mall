from typing import Optional

import dotenv
from ariadne import ObjectType
import os

from auth.signatures import get_last_user
from dto.authentication import Authentication

query = ObjectType("Query")

dotenv.load_dotenv(verbose=True, override=True)
LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")


@query.field("authentication")
def resolve_request_authentication(_, info) -> Optional[Authentication]:
    cookies = info.context['request'].cookies
    last_user = get_last_user()
    print("IN resolve_request_authentication - cookies, last_user:", cookies, last_user)
    if last_user == {}:
        return None

    address = last_user['address']
    return Authentication(address, address == LANDLORD_ADDR)
