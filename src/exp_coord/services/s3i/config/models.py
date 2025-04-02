from pydantic import BaseModel, Field

from exp_coord.core.annotations.s3i import S3IIdType


class PersonIdentity(BaseModel):
    username: str
    identifier: S3IIdType


class ThingIdentity(BaseModel):
    identifier: S3IIdType
    secret: str  # TODO: Add a validator here


class CreatePersonResponse(BaseModel):
    person: PersonIdentity = Field(alias="personIdentity")
    thing: ThingIdentity = Field(alias="thingIdentity")
