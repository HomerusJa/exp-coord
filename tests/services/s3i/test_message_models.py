import json
from pprint import pprint
from typing import Iterable

import pytest
from pathlib import Path

from exp_coord.services.s3i.message_models import S3IMessage


def get_broker_api_examples() -> Iterable[dict]:
    with open(Path(__file__).parent / "broker_api_swagger.json") as f:
        docs: dict = json.load(f)
    return map(lambda obj: obj["value"], docs["components"]["examples"].values())


@pytest.mark.parametrize("example", get_broker_api_examples())
def test_message_models(example: dict):
    """Test the message models against the broker API examples from the Swagger docs."""
    pprint(example)
    S3IMessage.validate_python(example)
