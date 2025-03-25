from typing import Literal, Union

from pydantic import BaseModel, TypeAdapter
from pydantic.types import JsonValue


class Attachment(BaseModel):
    """Model for message attachments.

    Attributes:
        filename (str): Name of the file.
        data (str): Base64-encoded file content.
    """

    filename: str
    data: str


class S3IUserMessage(BaseModel):
    """S³I user message model.

    Attributes:
        messageType (Literal["userMessage"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyToEndpoint (str): Reply endpoint.
        attachments (list[Attachment]): List of attachments.
        subject (str): Subject of the message.
        text (str): Body of the message.
    """

    messageType: Literal["userMessage"] = "userMessage"
    sender: str
    identifier: str
    receivers: list[str]
    replyToEndpoint: str
    attachments: list[Attachment]
    subject: str
    text: str


class S3IServiceRequest(BaseModel):
    """S³I service request model.

    Attributes:
        messageType (Literal["serviceRequest"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyToEndpoint (str): Reply endpoint for the service request.
        serviceType (str): Type of service requested.
        parameters (dict): Parameters for the service.
    """

    messageType: Literal["serviceRequest"] = "serviceRequest"
    sender: str
    identifier: str
    receivers: list[str]
    replyToEndpoint: str
    serviceType: str
    parameters: dict


class S3IServiceReply(BaseModel):
    """S³I service reply model.

    Attributes:
        messageType (Literal["serviceReply"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyingToMessage (str): Identifier of the referenced message.
        serviceType (str): Type of service.
        results (JsonValue): Result of the service.
    """

    messageType: Literal["serviceReply"] = "serviceReply"
    sender: str
    identifier: str
    receivers: list[str]
    replyingToMessage: str
    serviceType: str
    results: JsonValue


class S3IGetValueRequest(BaseModel):
    """S³I get value request model.

    Attributes:
        messageType (Literal["getValueRequest"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyToEndpoint (str): Reply endpoint for the request.
        attributePath (str): Path to the attribute.
    """

    messageType: Literal["getValueRequest"] = "getValueRequest"
    sender: str
    identifier: str
    receivers: list[str]
    replyToEndpoint: str
    attributePath: str


class S3IGetValueReply(BaseModel):
    """S³I get value reply model.

    Attributes:
        messageType (Literal["getValueReply"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyingToMessage (str): Identifier of the referenced message.
        value (JsonValue): Retrieved value.
    """

    messageType: Literal["getValueReply"] = "getValueReply"
    sender: str
    identifier: str
    receivers: list[str]
    replyingToMessage: str
    value: JsonValue


class S3ISetValueRequest(BaseModel):
    """S³I set value request model.

    Attributes:
        messageType (Literal["setValueRequest"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyToEndpoint (str): Reply endpoint for the request.
        attributePath (str): Path to the attribute.
        newValue (JsonValue): New value to set.
    """

    messageType: Literal["setValueRequest"] = "setValueRequest"
    sender: str
    identifier: str
    receivers: list[str]
    replyToEndpoint: str
    attributePath: str
    newValue: JsonValue


class S3ISetValueReply(BaseModel):
    """S³I set value reply model.

    Attributes:
        messageType (Literal["setValueReply"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyingToMessage (str): Identifier of the referenced message.
    """

    messageType: Literal["setValueReply"] = "setValueReply"
    sender: str
    identifier: str
    receivers: list[str]
    replyingToMessage: str


class S3ICreateAttributeRequest(BaseModel):
    """S³I create attribute request model.

    Attributes:
        messageType (Literal["createAttributeRequest"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyToEndpoint (str): Reply endpoint for the request.
        attributePath (str): Path to the attribute.
        newValue (str): Value of the new attribute.
    """

    messageType: Literal["createAttributeRequest"] = "createAttributeRequest"
    sender: str
    identifier: str
    receivers: list[str]
    replyToEndpoint: str
    attributePath: str
    newValue: str


class S3ICreateAttributeReply(BaseModel):
    """S³I create attribute reply model.

    Attributes:
        messageType (Literal["createAttributeReply"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyingToMessage (str): Identifier of the referenced message.
        ok (bool): Status of the operation.
    """

    messageType: Literal["createAttributeReply"] = "createAttributeReply"
    sender: str
    identifier: str
    receivers: list[str]
    replyingToMessage: str
    ok: bool


class S3IDeleteAttributeRequest(BaseModel):
    """S³I delete attribute request model.

    Attributes:
        messageType (Literal["deleteAttributeRequest"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyToEndpoint (str): Reply endpoint for the request.
        attributePath (str): Path to the attribute.
    """

    messageType: Literal["deleteAttributeRequest"] = "deleteAttributeRequest"
    sender: str
    identifier: str
    receivers: list[str]
    replyToEndpoint: str
    attributePath: str


class S3IDeleteAttributeReply(BaseModel):
    """S³I delete attribute reply model.

    Attributes:
        messageType (Literal["deleteAttributeReply"]): Type of the message.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
        replyingToMessage (str): Identifier of the referenced message.
        ok (bool): Status of the operation.
    """

    messageType: Literal["deleteAttributeReply"] = "deleteAttributeReply"
    sender: str
    identifier: str
    receivers: list[str]
    replyingToMessage: str
    ok: bool


S3IMessageType = Union[
    S3IUserMessage,
    S3IServiceRequest,
    S3IServiceReply,
    S3IGetValueRequest,
    S3IGetValueReply,
    S3ISetValueRequest,
    S3ISetValueReply,
    S3ICreateAttributeRequest,
    S3ICreateAttributeReply,
    S3IDeleteAttributeRequest,
    S3IDeleteAttributeReply,
]

S3IMessageAdapter = TypeAdapter(S3IMessageType)
MultipleS3IMessageAdapter = TypeAdapter(list[S3IMessageType])


class S3IEvent(BaseModel):
    """S³I event model.

    Attributes:
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for this event.
        timestamp (int): Unix timestamp of the event.
        topic (str): Topic associated with the event.
        messageType (Literal["event"]): Type of the message.
        content (JsonValue): Event content.
    """

    sender: str
    identifier: str
    timestamp: int
    topic: str
    messageType: Literal["eventMessage"] = "eventMessage"
    content: JsonValue


S3IEventAdapter = TypeAdapter(S3IEvent)
MultipleS3IEventAdapter = TypeAdapter(list[S3IEvent])
