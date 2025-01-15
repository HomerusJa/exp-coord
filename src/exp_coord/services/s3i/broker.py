from meatie import Request, endpoint, private, api_ref
from meatie_httpx import AsyncClient
import httpx
from typing import override, Annotated, Union

from exp_coord.core.config import Settings
from exp_coord.services.s3i.auth import KeycloakAuth
from exp_coord.services.s3i.message_models import S3IMessage, S3IEvent


class S3IBrokerEndpoint(AsyncClient):
    def __init__(
        self, settings: Settings | None = None, client: AsyncClient | None = None
    ):
        """Initialize the S³I Broker endpoint.

        Args:
            settings (Settings, optional): You could provide a custom settings object. Defaults to the global settings object.
            client (AsyncClient, optional): You could provide a custom HTTP client. Defaults to None.
        """
        if not settings:
            from exp_coord.core.config import settings

            settings = settings

        client = httpx.AsyncClient(
            # It is no problem to set the broker url here and use the client for the auth also, as it always
            # uses the full url overriding the base url.
            base_url=settings.s3i.broker_url,
        )
        self.auth = KeycloakAuth(
            http_client=client,
            keycloak_url=settings.s3i.auth_url,
            realm=settings.s3i.auth_realm,
            client_id=settings.s3i.client_id,
            client_secret=settings.s3i.client_secret,
        )
        super().__init__(client)

    @override
    async def authenticate(self, request: Request) -> None:
        """Authenticate the request using the Keycloak token."""
        token = await self.auth.get_valid_token()
        request.headers["Authorization"] = f"Bearer {token.access_token}"

    @endpoint("/{endpoint}", private)
    async def get(self, endpoint: str) -> S3IMessage: ...

    @endpoint("/{endpoint}/all", private)
    async def get_all(self, endpoint: str) -> list[S3IMessage]: ...

    @endpoint("/{endpoint}/event", private)
    async def get_event(self, endpoint: str) -> S3IEvent: ...

    @endpoint("/{endpoint}/event/all", private)
    async def get_all_events(self, endpoint: str) -> list[S3IEvent]: ...

    @endpoint("/{endpoints}", private)
    async def post(
        self,
        endpoints: list[str],
        message: Annotated[Union[S3IMessage, S3IEvent], api_ref("body")],
    ) -> None: ...


async def main():
    endpoint = S3IBrokerEndpoint()
    content = {
        "messageType": "getValueRequest",
        "sender": "test",
        "identifier": "test",
        "receivers": ["test"],
        "replyToEndpoint": "test",
        "attributePath": "test",
    }
    await endpoint.post(
        ["endpoint1", "endpoint2"], message=S3IMessage.validate_python(content)
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
