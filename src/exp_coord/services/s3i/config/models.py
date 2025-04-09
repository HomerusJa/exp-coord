from pydantic import BaseModel, Field, Secret

from exp_coord.core.annotations.s3i import S3IIdType


class PersonIdentity(BaseModel):
    username: str
    identifier: S3IIdType
    password: Secret[str] | None = None


class ThingIdentity(BaseModel):
    identifier: S3IIdType
    secret: Secret[str]  # TODO: Add a validator here


class FullIdentity(BaseModel):
    person: PersonIdentity = Field(alias="personIdentity")
    thing: ThingIdentity = Field(alias="thingIdentity")
