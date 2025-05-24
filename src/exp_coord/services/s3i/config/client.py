from loguru import logger
from pydantic import validate_call

from exp_coord.core.config import S3ISettings
from exp_coord.services.s3i.base.annotations import S3IIdType
from exp_coord.services.s3i.base.client import BaseS3IClient
from exp_coord.services.s3i.config.models import FullIdentity


class S3IConfigClient(BaseS3IClient):
    """A client for interfacing with the S3I config API, specified under https://config.s3i.vswf.dev/apidoc/"""

    def __init__(self, settings: S3ISettings) -> None:
        super().__init__(settings, settings.config_url)

        # Rudimentary check for permission => check that person who is authing is not a thing, but a person
        if not self.auth.is_person:
            logger.warning(
                "The authenticated entity is apparently not a person. You will most certainly run into problems with your level of permission."
            )

    async def create_person(self, username: str, password: str) -> FullIdentity:
        if username.lower() != username:
            raise ValueError("The username must be lowercase.")
        response = await self._send_request(
            "POST",
            "/persons/",
            log_response=False,  # Raw secret is sent in response
            json={"username": username, "password": password},
        )
        return FullIdentity.model_validate_json(response.content)

    async def query_person(self, username: str) -> FullIdentity | None:
        response = await self._send_request(
            "GET", f"/persons/{username}", extend_allowed_response_codes=[404]
        )
        if response.status_code == 404:
            return None
        return FullIdentity.model_validate_json(response.content)

    async def delete_person(self, username: str):
        _ = await self._send_request("DELETE", f"/persons/{username}")

    @validate_call
    async def create_thing_event_queue(
        self, thing_id: S3IIdType, topic: str, queue_length: int = 0, ttl: int = 0
    ):
        _ = await self._send_request(
            "POST",
            f"/things/{thing_id}/event-queues",
            json={"topic": topic, "queue_length": queue_length, "ttl": ttl},
        )

    @validate_call
    async def delete_thing_event_queue(self, thing_id: S3IIdType) -> None:
        _ = await self._send_request("DELETE", f"/things/{thing_id}/broker/event")

    @validate_call
    async def add_thing_event_topics(self, thing_id: S3IIdType, topic: str) -> None:
        # TODO: Check if multiple topics are allowed
        _ = await self._send_request(
            "POST", f"/things/{thing_id}/broker/event", json={"topic": [topic]}
        )

    # Missing endpoints:
    # POST /things/
    # GET /things/{thingId}
    # PUT /things/{thingId}
    # DELETE /things/{thingId}
    # POST /things/{thingId}/repository
    # DELETE /things/{thingId}/repository
    # POST /things/{thingId}/broker
    # DELETE /things/{thingId}/broker
