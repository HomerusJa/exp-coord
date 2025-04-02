from exp_coord.core.config import S3ISettings
from exp_coord.services.s3i.base.client import BaseS3IClient
from exp_coord.services.s3i.config.models import CreatePersonResponse


class S3IConfigClient(BaseS3IClient):
    """A client for interfacing with the S3I config API, specified under https://config.s3i.vswf.dev/apidoc/"""

    def __init__(self, settings: S3ISettings) -> None:
        super().__init__(settings, settings.config_url)

    async def create_person(self, username: str, password: str) -> CreatePersonResponse:
        if username.lower() != username:
            raise ValueError("The username must be lowercase.")
        return self._send_request(
            "POST",
            "/persons/",
            CreatePersonResponse,
            json={"username": username, "password": password},
        )

    async def query_person(self, username: str) -> str:
        return self._send_request("GET", f"/persons/{username}", None)
