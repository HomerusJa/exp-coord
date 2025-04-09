from pydantic import validate_call

from exp_coord.core.annotations.s3i import S3IMessageQueueType
from exp_coord.core.config import S3ISettings
from exp_coord.core.utils import _get_type_adapter
from exp_coord.services.s3i.base.client import BaseS3IClient
from exp_coord.services.s3i.broker.models import (
    S3IEvent,
    S3IMessage,
)


class S3IBrokerClient(BaseS3IClient):
    """An asynchronous implementation of the S³I api specification.

    The API is defined at https://broker.s3i.vswf.dev/apidoc/
    """

    def __init__(self, settings: S3ISettings) -> None:
        super().__init__(settings, settings.broker_url)

    async def receive_message(self) -> S3IMessage | None:
        """Receive a message from the S³I Broker.

        Raises:
            S3IBrokerError: If the broker responds with an error.

        Returns:
            Optional[S3IMessage]: The received message, if received.
        """
        response = await self._send_request("GET", f"/{self.settings.message_queue}")
        if len(response.content) == 0:
            return None
        _get_type_adapter(S3IMessage).validate_json(response.content)

    async def receive_all_messages(self) -> list[S3IMessage]:
        """Receive all messages from the S³I Broker.

        Raises:
            S3IBrokerError: If the broker responds with an error.

        Returns:
            list[S3IMessage]: The received messages.
        """
        response = await self._send_request("GET", f"/{self.settings.message_queue}/all")
        return _get_type_adapter(list[S3IMessage]).validate_json(response.content)

    async def receive_event(self) -> S3IEvent | None:
        """Receive an event from the S³I Broker.

        Raises:
            S3IBrokerError: If the broker responds with an error.

        Returns:
            Optional[S3IEvent]: The received event, if received.
        """
        response = await self._send_request("GET", f"/{self.settings.event_queue}")
        if len(response.content) == 0:
            return None
        _get_type_adapter(S3IEvent).validate_json(response.content)

    async def receive_all_events(self) -> list[S3IEvent]:
        """Receive all events from the S³I Broker.

        Raises:
            S3IBrokerError: If the broker responds with an error.

        Returns:
            list[S3IEvent]: The received events.
        """
        response = await self._send_request("GET", f"/{self.settings.event_queue}/all")
        return _get_type_adapter(list[S3IEvent]).validate_json(response.content)

    @validate_call
    async def send_message(
        self, endpoint: S3IMessageQueueType | list[S3IMessageQueueType], message: S3IMessage
    ) -> None:
        """Send a message to the S³I Broker.

        Args:
            endpoint (S3I_Message_Queue): The endpoint to send the message to.
            message (S3IMessage): The message to send.

        Raises:
            S3IBrokerError: If the broker responds with an error.
        """
        endpoint = endpoint if isinstance(endpoint, str) else ",".join(endpoint)
        await self._send_request("POST", f"/{endpoint}", content=message.model_dump_json())

    @validate_call
    async def send_event(self, event: S3IEvent) -> None:
        """Send an event to the S³I Broker.

        Args:
            event (S3IEvent): The event to send.

        Raises:
            S3IBrokerError: If the broker responds with an error.
        """
        await self.client.post(f"/{event.topic}", content=event.model_dump_json())
