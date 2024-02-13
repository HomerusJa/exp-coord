"""Defines the entities like they are in the S3I-Infrastructure.

Entities:
    Person(username, password)
    Thing(id, secret, queue)
"""

from dataclasses import dataclass


@dataclass
class Person:
    """A basic person in the S3I-Infrastructure.

    Args:
        username (str): The username of the person.
        password (str): The password of the person.
    """
    username: str
    password: str


@dataclass
class Thing:
    """A basic thing in the S3I-Infrastructure.

    Args:
        id (str): The id of the thing.
        secret (str): The secret of the thing.
        queue (str): The queue of the thing.
    """
    id: str
    secret: str
    queue: str
