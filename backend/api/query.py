from typing import Optional

from ariadne import ObjectType

from dto.authentication import Authentication

query = ObjectType("Query")


@query.field("authentication")
def resolve_request_authentication(_, info) -> Optional[Authentication]:
    cookies = info.context['request'].cookies
    address = cookies.get('address')
    if address not in cookies:
        return None

    return Authentication("test_address_1", True) # TODO
