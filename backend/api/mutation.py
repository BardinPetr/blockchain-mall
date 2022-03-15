import os

import dotenv
from ariadne import ObjectType
from dto.authentication import Authentication

from backend.error.exceptions import AuthenticationFailed
from backend.web3.signatures import create_message, restore_signer

mutation = ObjectType("Mutation")

dotenv.load_dotenv(verbose=True, override=True)
LANDLORD_ADDR = os.getenv("LANDLORD_ADDRESS")


@mutation.field("requestAuthentication")
def resolve_request_authentication(_, info, address: str) -> str:
    return create_message(address)


@mutation.field("authenticate")
def resolve_authenticate(_, info, address: str, signedMessage: dict):
    try:
        address = address.lower()
        restored_addr = restore_signer(address, signedMessage).lower()
        if restored_addr == address:
            return Authentication(address, address == LANDLORD_ADDR.lower())
    except:
        pass
    raise AuthenticationFailed()
