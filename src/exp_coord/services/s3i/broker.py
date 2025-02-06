from typing import Annotated, Optional, Union, override

import httpx
from loguru import logger
from meatie import (
    AsyncResponse,
    Request,
    api_ref,
    body,
    endpoint,
    private,
)
from meatie_httpx import AsyncClient
from pydantic import BaseModel, TypeAdapter

from exp_coord.core.config import settings
from exp_coord.core.utils import PydanticModel
from exp_coord.services.s3i.auth import KeycloakAuth
from exp_coord.services.s3i.error import get_error
from exp_coord.services.s3i.message_models import S3IEvent, S3IMessage


class S3IBrokerClient(AsyncClient):
    def __init__(self):
        """Initialize the S³I Broker endpoint."""
        client = httpx.AsyncClient(
            base_url=settings.s3i.broker_url,
            timeout=30.0,  # Add timeout for safety
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
        request.headers["Authorization"] = f"Bearer {token}"

    async def _process_single_response(
        self,
        response: AsyncResponse,
        model_class: PydanticModel,
        endpoint: str,
        entity_type: str,
    ) -> Optional[PydanticModel]:
        """Process a single entity response."""
        text = await response.text()
        if not text:
            logger.info(f"No {entity_type}s available for endpoint {endpoint}.")
            return None
        if isinstance(model_class, BaseModel):
            return model_class.model_validate_json(text)
        elif isinstance(model_class, TypeAdapter):
            return model_class.validate_json(text)
        else:
            raise ValueError("Model class must be a Pydantic model or a Type Adapter.")

    async def get_message(self, endpoint: str) -> Optional[S3IMessage]:
        """Get a message from the broker."""
        response = await self._get_message(endpoint=endpoint)
        return await self._process_single_response(response, S3IMessage, endpoint, "message")

    @endpoint("/{endpoint}", private, body(error=get_error))
    async def _get_message(self, endpoint: str) -> AsyncResponse: ...

    @endpoint("/{endpoint}/all", private, body(error=get_error))
    async def get_all_messages(self, endpoint: str) -> list[S3IMessage]: ...

    async def get_event(self, endpoint: str) -> Optional[S3IEvent]:
        """Get an event from the broker."""
        response = await self._get_event(endpoint=endpoint)
        return await self._process_single_response(response, S3IEvent, endpoint, "event")

    @endpoint("/{endpoint}/event", private, body(error=get_error))
    async def _get_event(self, endpoint: str) -> AsyncResponse: ...

    @endpoint("/{endpoint}/event/all", private, body(error=get_error))
    async def get_all_events(self, endpoint: str) -> list[S3IEvent]: ...

    # TODO: Implement response handling.
    # The response is pretty detailed and should be handled properly.
    # https://broker.s3i.vswf.dev/apidoc/#/Broker/post__endpoints_
    @endpoint("/{endpoints}", private, body(error=get_error))
    async def post(
        self,
        endpoints: list[str],
        message: Annotated[Union[S3IMessage, S3IEvent], api_ref("body")],
    ) -> None: ...  # type: ignore[empty-body]
