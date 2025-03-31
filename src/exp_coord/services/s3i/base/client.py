from typing import Any

import httpx
from pydantic import TypeAdapter

from exp_coord.core.config import S3ISettings
from exp_coord.services.s3i.base.auth import KeycloakAuth
from exp_coord.services.s3i.broker.error import raise_on_error


def _create_auth_from_settings(client: httpx.AsyncClient, settings: S3ISettings) -> KeycloakAuth:
    return KeycloakAuth(
        http_client=client,
        keycloak_url=settings.auth_url,
        realm=settings.auth_realm,
        client_id=settings.client_id,
        client_secret=settings.client_secret,
    )


class BaseS3IClient:
    """The base client, providing the boilerplate for the other clients further down the road."""

    def __init__(self, settings: S3ISettings, base_url: str) -> None:
        self.settings = settings
        self.auth = _create_auth_from_settings(httpx.AsyncClient(), settings)
        self.client = httpx.AsyncClient(base_url=base_url, auth=self.auth)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aclose()

    async def aclose(self) -> None:
        await self.client.aclose()

    async def _send_request(self, method: str, endpoint: str, response_adapter: TypeAdapter) -> Any:
        """Send a  request to the specified endpoint and deserialize the response.

        Args:
            method (str): The HTTP method to use.
            endpoint (str): The endpoint to send the request to.
            response_adapter (TypeAdapter): The response adapter to use.

        Returns:
            Any: The deserialized response.
        """
        response = await self.client.request(method, endpoint)
        await raise_on_error(response)

        if response.content == b"":
            return None

        # This might as well work, but I am doing this for consistency
        if response.content == b"[]":
            return []

        return response_adapter.validate_json(response.content)
