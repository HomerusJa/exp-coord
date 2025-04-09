from loguru import logger

from exp_coord.core.config import S3ISettings
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
            json={"username": username, "password": password},
        )
        return FullIdentity.model_validate_json(response)

    async def query_person(self, username: str) -> FullIdentity | None:
        response = await self._send_request(
            "GET", f"/persons/{username}", extend_allowed_response_codes=[404]
        )
        if response.status_code == 404:
            return None
        return FullIdentity.model_validate_json(response.content)

    async def delete_person(self, username: str):
        _ = await self._send_request("DELETE", f"/persons/{username}")
