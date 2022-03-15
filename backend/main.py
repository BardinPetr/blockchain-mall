import os
import sys

from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route

from api.mutation import mutation
from api.query import query
from error.error_formatter import simple_format_error

module_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
if module_path not in sys.path:
    sys.path.append(module_path)
import uvicorn


async def main(request):
    full_path = request.path_params['full_path']
    print("Request full_path: " + full_path)
    if full_path == 'graphql' or full_path == "graphql/":
        return gql


schema = load_schema_from_path("../schema.graphql")
print("Schema=" + str(schema))
executable_schema = make_executable_schema(
    schema,
    [query,
     mutation])


gql = GraphQL(executable_schema, debug=False, error_formatter=simple_format_error)
app = Starlette(
    routes=[
        Route('/{full_path:path}', main, methods=["GET", "POST", "OPTIONS"]),
    ],
    middleware=[
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=("GET", "POST", "OPTIONS"))
    ]
)

if __name__ == "__main__":
    print("Starting...")
    uvicorn.run("main:app", host="0.0.0.0", port=81)