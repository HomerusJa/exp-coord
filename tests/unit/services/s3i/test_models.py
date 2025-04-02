import json
from pathlib import Path
from typing import Iterable

import pytest
from pydantic import TypeAdapter

from exp_coord.services.s3i.broker.models import S3IMessage


def get_broker_api_examples() -> Iterable[dict]:
    with open(Path(__file__).parent / "broker_api_swagger.json") as f:
        docs: dict = json.load(f)
    return (obj["value"] for obj in docs["components"]["examples"].values())


@pytest.fixture(scope="session")
def s3i_message_adapter() -> TypeAdapter[S3IMessage]:
    return TypeAdapter(S3IMessage)


@pytest.mark.parametrize("example", get_broker_api_examples())
def test_message_models(example: dict, s3i_message_adapter):
    """Test the message models against the broker API examples from the Swagger docs."""
    s3i_message_adapter.validate_python(example)
