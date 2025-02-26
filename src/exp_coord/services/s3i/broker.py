from typing import Any

import httpx
from pydantic import TypeAdapter, validate_call

from exp_coord.core.annotations.s3i import S3IMessageQueueType
from exp_coord.core.config import S3ISettings
from exp_coord.services.s3i.auth import KeycloakAuth
from exp_coord.services.s3i.error import raise_on_error
from exp_coord.services.s3i.models import (
    MultipleS3IEventAdapter,
    MultipleS3IMessageAdapter,
    S3IEvent,
    S3IEventAdapter,
    S3IMessageAdapter,
    S3IMessageType,
)


def _create_auth_from_settings(client: httpx.AsyncClient, settings: S3ISettings) -> KeycloakAuth:
    return KeycloakAuth(
        http_client=client,
        keycloak_url=settings.auth_url,
        realm=settings.auth_realm,
        client_id=settings.client_id,
        client_secret=settings.client_secret,
    )


class S3IBrokerClient:
    """An asynchronous implementation of the S³I api specification.

    The API is defined at https://broker.s3i.vswf.dev/apidoc/
    """

    def __init__(self, settings: S3ISettings) -> None:
        self.settings = settings
        self.auth = _create_auth_from_settings(httpx.AsyncClient(), settings)
        self.client = httpx.AsyncClient(base_url=settings.broker_url, auth=self.auth)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        await self.auth.aclose()
        await self.client.aclose()

    async def _send_request(self, method: str, endpoint: str, response_adapter: TypeAdapter) -> Any:
        response = await self.client.request(method, endpoint)
        await raise_on_error(response)

        if response.content == b"":
            return None

        # This might as well work, but I am doing this for consistency
        if response.content == b"[]":
            return []

        return response_adapter.validate_json(response.content)

    async def receive_message(self) -> S3IMessageType | None:
        """Receive a message from the S³I Broker.

        Raises:
            S3IBrokerError: If the broker responds with an error.

        Returns:
            Optional[S3IMessage]: The received message, if received.
        """
        return await self._send_request("GET", f"/{self.settings.message_queue}", S3IMessageAdapter)

    async def receive_all_messages(self) -> list[S3IMessageType]:
        """Receive all messages from the S³I Broker.

        Raises:
            S3IBrokerError: If the broker responds with an error.

        Returns:
            list[S3IMessage]: The received messages.
        """
        return await self._send_request(
            "GET", f"/{self.settings.message_queue}/all", MultipleS3IMessageAdapter
        )

    async def receive_event(self) -> S3IEvent | None:
        """Receive an event from the S³I Broker.

        Raises:
            S3IBrokerError: If the broker responds with an error.

        Returns:
            Optional[S3IEvent]: The received event, if received.
        """
        return await self._send_request("GET", f"/{self.settings.event_queue}", S3IEventAdapter)

    async def receive_all_events(self) -> list[S3IEvent]:
        """Receive all events from the S³I Broker.

        Raises:
            S3IBrokerError: If the broker responds with an error.

        Returns:
            list[S3IEvent]: The received events.
        """
        return await self._send_request(
            "GET", f"/{self.settings.event_queue}/all", MultipleS3IEventAdapter
        )

    @validate_call
    async def send_message(
        self, endpoint: S3IMessageQueueType | list[S3IMessageQueueType], message: S3IMessageType
    ) -> None:
        """Send a message to the S³I Broker.

        Args:
            endpoint (S3I_Message_Queue): The endpoint to send the message to.
            message (S3IMessage): The message to send.

        Raises:
            S3IBrokerError: If the broker responds with an error.
        """
        endpoint = endpoint if isinstance(endpoint, str) else ",".join(endpoint)
        response = await self.client.post(f"/{endpoint}", content=message.model_dump_json())
        await raise_on_error(response)

    @validate_call
    async def send_event(self, event: S3IEvent) -> None:
        """Send an event to the S³I Broker.

        Args:
            event (S3IEvent): The event to send.

        Raises:
            S3IBrokerError: If the broker responds with an error.
        """
        response = await self.client.post(f"/{event.topic}", content=event.model_dump_json())
        await raise_on_error(response)


async def main():
    from exp_coord.core.config import settings

    async with S3IBrokerClient(settings.s3i) as client:
        message = await client.receive_message()
        print(message)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
