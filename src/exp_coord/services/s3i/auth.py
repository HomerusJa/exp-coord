from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import httpx
from loguru import logger


@dataclass
class TokenData:
    access_token: str
    refresh_token: str | None
    expires_at: datetime


class KeycloakAuth:
    def __init__(
        self,
        http_client: httpx.AsyncClient,
        keycloak_url: str,
        realm: str,
        client_id: str,
        client_secret: str,
        username: str | None = None,
        password: str | None = None,
        token_refresh_margin: timedelta = timedelta(minutes=1),
    ) -> None:
        self.token_url = (
            f"{keycloak_url.rstrip("/")}/realms/{realm}/protocol/openid-connect/token"
        )

        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.client = http_client
        self.token_refresh_margin = token_refresh_margin
        self._token_data: TokenData | None = None

    async def get_new_token(self) -> TokenData:
        """Get initial token using configured grant type."""
        if self.username and self.password:
            data = {
                "grant_type": "password",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": self.username,
                "password": self.password,
            }
        else:
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

        response = await self.client.post(self.token_url, data=data)
        response.raise_for_status()
        token_data = response.json()

        logger.success("Got an initial token.")

        return TokenData(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=token_data["expires_in"]),
        )

    async def refresh_auth_token(self, refresh_token: str) -> TokenData:
        """Refresh the access token using the refresh token."""
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }

        response = await self.client.post(self.token_url, data=data)
        response.raise_for_status()
        token_data = response.json()

        logger.success("Refreshed token.")

        return TokenData(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=token_data["expires_in"]),
        )

    def _is_token_valid(self, token: TokenData) -> bool:
        """Check if token is valid and not near expiry."""
        return datetime.now(timezone.utc) + self.token_refresh_margin < token.expires_at

    async def get_valid_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        if not self._token_data or not self._is_token_valid(self._token_data):
            logger.debug("Current token is invalid or expired.")
            try:
                if self._token_data and self._token_data.refresh_token:
                    self._token_data = await self.refresh_auth_token(
                        self._token_data.refresh_token
                    )
                else:
                    self._token_data = await self.get_new_token()
            except httpx.HTTPError:
                # If refresh fails, try getting a new token
                self._token_data = await self.get_new_token()

        logger.success("Got a valid token.")
        return self._token_data.access_token

    async def auth_flow(self, request: httpx.Request) -> httpx.Request:
        """Authentication flow for HTTPX AuthFlow protocol."""
        token = await self.get_valid_token()
        request.headers["Authorization"] = f"Bearer {token}"
        return request
