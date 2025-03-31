from exp_coord.core.config import S3ISettings
from exp_coord.services.s3i.base.client import BaseS3IClient


class S3IConfigClient(BaseS3IClient):
    """A client for interfacing with the S3I config API, specified under https://config.s3i.vswf.dev/apidoc/"""

    def __init__(self, settings: S3ISettings) -> None:
        super().__init__(settings, settings.config_url)

    async def create_person(self, username: str, password: str): ...
