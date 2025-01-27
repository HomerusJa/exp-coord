import pytest
import httpx
from datetime import datetime, timedelta, timezone
from exp_coord.services.s3i.auth import KeycloakAuth, TokenData
import pytest_asyncio


@pytest.fixture
def auth_config():
    """Fixture providing a basic KeycloakAuth configuration."""
    return {
        "keycloak_url": "https://keycloak.example.com",
        "realm": "myrealm",
        "client_id": "test-client",
        "client_secret": "test-secret",
        "username": "test-user",
        "password": "test-password",
    }


@pytest_asyncio.fixture()
async def http_client():
    """Fixture for an async HTTP client."""
    async with httpx.AsyncClient() as client:
        yield client


@pytest.mark.asyncio
async def test_get_new_token(respx_mock, http_client, auth_config):
    """Test fetching a new token."""
    respx_mock.post(
        f"{auth_config['keycloak_url']}/realms/{auth_config['realm']}/protocol/openid-connect/token"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 3600,
            },
        )
    )

    auth = KeycloakAuth(http_client=http_client, **auth_config)
    token_data = await auth.get_new_token()

    assert token_data.access_token == "new_access_token"
    assert token_data.refresh_token == "new_refresh_token"
    assert token_data.expires_at > datetime.now(timezone.utc)


@pytest.mark.asyncio
async def test_refresh_auth_token(respx_mock, http_client, auth_config):
    """Test refreshing an access token."""
    respx_mock.post(
        f"{auth_config['keycloak_url']}/realms/{auth_config['realm']}/protocol/openid-connect/token"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "refreshed_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 3600,
            },
        )
    )

    auth = KeycloakAuth(http_client=http_client, **auth_config)
    token_data = await auth.refresh_auth_token("test_refresh_token")

    assert token_data.access_token == "refreshed_access_token"
    assert token_data.refresh_token == "new_refresh_token"
    assert token_data.expires_at > datetime.now(timezone.utc)


@pytest.mark.asyncio
async def test_get_valid_token_with_refresh(respx_mock, http_client, auth_config):
    """Test getting a valid token, including refresh."""
    respx_mock.post(
        f"{auth_config['keycloak_url']}/realms/{auth_config['realm']}/protocol/openid-connect/token"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 3600,
            },
        )
    )

    auth = KeycloakAuth(http_client=http_client, **auth_config)

    # First call should get a new token
    token = await auth.get_valid_token()
    assert token == "new_access_token"

    # Simulate token near expiry
    auth._token_data = TokenData(
        access_token="old_access_token",
        refresh_token="old_refresh_token",
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=5),
    )

    # Next call should refresh the token
    token = await auth.get_valid_token()
    assert token == "new_access_token"


@pytest.mark.asyncio
async def test_auth_flow(respx_mock, http_client, auth_config):
    """Test the auth_flow method."""
    respx_mock.post(
        f"{auth_config['keycloak_url']}/realms/{auth_config['realm']}/protocol/openid-connect/token"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 3600,
            },
        )
    )

    auth = KeycloakAuth(http_client=http_client, **auth_config)

    request = httpx.Request("GET", "https://example.com")
    authorized_request = await auth.auth_flow(request)

    assert authorized_request.headers["Authorization"] == "Bearer new_access_token"
