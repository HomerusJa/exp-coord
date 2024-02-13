import logging
from typing import Protocol

import requests

from exp_coord.tasks.s3i.entities import Person, Thing


class Authenticator(Protocol):
    """A basic Protocol for an authenticator"""

    def get_auth_headers(self) -> dict:
        """Function to perform the actual authorization.

        Returns:
            dict: headers which should be sent.
        """
        ...


class JWTAuthenticator:
    """This is the main Authenticator in the S3I-ecosystem which works according to the Authenticator-Protocol above"""

    def __init__(
            self,
            person: Person,
            thing: Thing,
            auth_url: str = "https://idp.s3i.vswf.dev/auth/realms/KWH/protocol/openid-connect/token",
            logger: logging.Logger = logging.getLogger("S3I"),
    ) -> None:
        self.person = person
        self.thing = thing
        self.auth_url = auth_url
        self._logger = logger

    def get_auth_headers(self) -> dict:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self._logger.debug(f"Headers: {headers}")

        payload = {
            "grant_type": "password",
            "username": self.person.username,
            "password": self.person.password,
            "client_id": self.thing.id,
            "client_secret": self.thing.secret,
        }
        self._logger.debug(f"Payload: {payload}")

        resp = requests.post(
            self.auth_url,
            data=payload,
            headers=headers,
        )
        self._logger.debug(f"Response: {resp.text}")
        answer = resp.json()

        return {
            "Authorization": f"{answer["token_type"]} {answer["access_token"]}",
        }


class NoAuthAuthenticator:
    """This is a basic Authenticator which does not perform any authorization. It works according to the Authenticator-
    Protocol above.
    """

    def get_auth_headers(self) -> dict:
        return {}
