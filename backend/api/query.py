from typing import Optional

import dotenv
from ariadne import ObjectType
import os

from dto.authentication import Authentication

query = ObjectType("Query")

dotenv.load_dotenv(verbose=True, override=True)
LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")


@query.field("authentication")
def resolve_request_authentication(_, info) -> Optional[Authentication]:
    cookies = info.context['request'].cookies
    address = cookies.get('address')
    if address not in cookies:
        return None

    return Authentication(address, address == LANDLORD_ADDR)
