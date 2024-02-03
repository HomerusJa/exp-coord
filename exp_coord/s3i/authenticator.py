import json
from typing import Protocol

import requests
from entities import Person, Thing


class Authenticator(Protocol):
    """A basic Protocol for an authenticator"""

    def getAuthHeaders() -> dict:
        """Function to perform the actual authorization.

        Returns:
            dict: headers which should be sent.
        """
        ...


class JWTAuthenticator:
    """This is a basic JWT-Authenticator which works according to the Authenticator-Protocol above"""

    def __init__(
        self,
        person: Person,
        thing: Thing,
        auth_url: str = "https://idp.s3i.vswf.dev/auth/realms/KWH/protocol/openid-connect/token",
    ) -> None:
        self.person = person
        self.thing = thing
        self.auth_url = auth_url

    def getAuthHeaders(self) -> dict:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        payload = {
            "grant_type": "password",
            "username": self.person.username,
            "password": self.person.password,
            "client_id": self.thing.id,
            "client_secret": self.thing.secret,
        }

        r = requests.post(
            self.auth_url,
            data=payload,
            headers=headers,
        )
        answer = json.loads(r.text)

        return {
            "Authorization": f"{answer["token_type"]} {answer["access-token"]}",
        }
