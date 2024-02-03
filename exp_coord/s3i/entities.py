"""Defines the entities like they are in the S3I-Infastructure.

Entities:
    Person(username, password)
    Thing(id, secret, queue)
"""

from collections import namedtuple


Person = namedtuple("Person", {"username", "password"})
Thing = namedtuple("Thing", {"id", "secret", "queue"})