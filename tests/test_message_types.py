import re

from exp_coord.tasks.s3i import message_types


def test__generate_identifier():
    ident1 = message_types._generate_identifier()
    ident2 = message_types._generate_identifier()

    pattern = re.compile(r'^s3i:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    assert pattern.match(ident1) is not None, f"Identifier format is invalid. The identifier is: {ident1}"
    assert pattern.match(ident2) is not None, f"Identifier format is invalid. The identifier is: {ident2}"

    assert ident1 != ident2, f"Identifiers are equal, but they should be unique. ident1: {ident1}, ident2: {ident2}"
