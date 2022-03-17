import os
import sys

from ariadne import graphql_sync, make_executable_schema
from ariadne import load_schema_from_path
from ariadne.asgi import GraphQL
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify, session as f_session, make_response
from flask_cors import CORS

from api.mutation import mutation
from api.query import query
from error.error_formatter import simple_format_error

module_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
if module_path not in sys.path:
    sys.path.append(module_path)

schema = load_schema_from_path("schema.graphql")
# print("Schema =" + schema)
executable_schema = make_executable_schema(schema, [query, mutation])

gql = GraphQL(executable_schema, debug=False, error_formatter=simple_format_error)

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()
CORS(app,
     supports_credentials=True,
     expose_headers=["Set-Cookie"],
     allow_headers="*",
     methods=["GET", "POST", "OPTIONS"],
     origins=['http://localhost:81',
              'http://localhost:82',
              'http://localhost:3000',
              'http://0.0.0.0:8089'])


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        executable_schema,
        data,
        context_value=request,
        debug=app.debug
    )

    resp = make_response(jsonify(result))
    resp.status_code = 200 if success else 400

    token = f_session.get("set_token")
    if token is not None:
        resp.set_cookie("access_token_cookie", token)

    return resp


if __name__ == "__main__":
    print("Starting...")
    print("LANDLORD_ADDRESS=" + str(os.getenv("LANDLORD_ADDRESS")))
    # uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "81")))
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", "81")))
