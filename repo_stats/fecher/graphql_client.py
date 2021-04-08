import os
from typing import List

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport


def graphql_connection():
    def check_env(variables: List[str]):
        for variable in variables:
            if os.getenv(variable) is None:
                raise EnvironmentError(f"Variable {variable} isn't set.")

    check_env(["ENDPOINT", "TOKEN"])
    url = os.getenv("ENDPOINT")
    token = os.getenv("TOKEN")

    headers = {"Authorization": f"bearer {token}"}
    transport = AIOHTTPTransport(url=url, headers=headers)
    return Client(transport=transport, fetch_schema_from_transport=True)
