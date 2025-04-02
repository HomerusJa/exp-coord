from typing import Any, AsyncIterable, Iterable

import httpx

from exp_coord.core.config import S3ISettings
from exp_coord.services.s3i.base.auth import KeycloakAuth
from exp_coord.services.s3i.base.error import raise_on_error


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

    async def _send_request(
        self,
        method: str,
        endpoint: str,
        *,
        content: str | bytes | Iterable[bytes] | AsyncIterable[bytes] | None = None,
        **extra_request_kwargs: Any,
    ) -> bytes:
        """Send a  request to the specified endpoint and deserialize the response.

        Args:
            method (str): The HTTP method to use.
            endpoint (str): The endpoint to send the request to.
            response_adapter (TypeAdapter | Any | None):
                Either an already instantiated TypeAdapter, or a type other than None in which case
                a cached TypeAdapter instance will be created, or None, when the response content
                will be returned as is.
            content (str): The content to send in the request.
            **extra_request_kwargs: Extra kwargs passed to httpx.AsyncClient.request()

        Returns:
            `T` if `response_adapter` is provided.
        """
        response = await self.client.request(
            method, endpoint, content=content, **extra_request_kwargs
        )
        await raise_on_error(response)

        return response.content
