from ariadne import ObjectType

from dto.authentication import Authentication

mutation = ObjectType("Mutation")


@mutation.field("requestAuthentication")
def resolve_request_authentication(_, info, address: str) -> str:
    return address  # TODO


@mutation.field("authenticate")
def resolve_authenticate(_, info, address: str, signedMessage: dict) -> Authentication:
    return Authentication("test_address", True)  # TODO
