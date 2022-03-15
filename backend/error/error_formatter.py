from ariadne import format_error
from graphql import GraphQLError


def simple_format_error(error: GraphQLError, debug: bool = False) -> dict:
    if debug:
        return format_error(error, debug)

    formatted = error.formatted
    del formatted["locations"]
    del formatted["path"]

    return formatted