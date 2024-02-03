import requests
from s3i.authenticator import Authenticator
from s3i.entities import Thing
import logging


class S3IClient:
    def __init__(self, endpoint: Thing, auth: Authenticator, logger):
        self.endpoint = endpoint
        self.authenticator = auth

    def receive_message(self, all=False) -> requests.Response | list[requests.Response]:
        headers = {}
        headers |= self.authenticator.getAuthHeaders()
        response = requests.get(
            f"https://broker.s3i.vswf.dev/{self.endpoint.queue}{"/all" if all else ""}",
            headers=headers,
        )
        self._validate_receive_message(response)        
        return response
    
    def _validate_receive_message(self, resp) -> :
        pass
        