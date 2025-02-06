from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, Field, TypeAdapter

__all__ = ["S3IEvent", "S3IMessage"]


class S3IMessageBase(BaseModel):
    """Base class for all S³I messages.

    Attributes:
        messageType (str): The type of message, defined by subclasses.
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for the message.
        receivers (list[str]): List of message receivers.
    """

    messageType: str
    sender: str
    identifier: str
    receivers: list[str]


class Attachment(BaseModel):
    """Model for message attachments.

    Attributes:
        filename (str): Name of the file.
        data (str): Base64-encoded file content.
    """

    filename: str
    data: str


class ReplyableMessage(S3IMessageBase):
    """Base class for messages that require a reply endpoint.

    Attributes:
        replyToEndpoint (str): Endpoint for message replies.
    """

    replyToEndpoint: str


class ReplyMessage(S3IMessageBase):
    """Base class for messages that reference a previous message.

    Attributes:
        replyingToMessage (str): Identifier of the referenced message.
    """

    replyingToMessage: str


class AttributeMessage(ReplyableMessage):
    """Base class for messages involving attribute paths.

    Attributes:
        attributePath (str): Path to the attribute.
    """

    attributePath: str


class S3IUserMessage(S3IMessageBase):
    """S³I user message model.

    Attributes:
        messageType (Literal["userMessage"]): Type of the message.
        replyToEndpoint (str): Reply endpoint.
        attachments (list[Attachment]): List of attachments.
        subject (str): Subject of the message.
        text (str): Body of the message.
    """

    messageType: Literal["userMessage"] = "userMessage"
    replyToEndpoint: str
    attachments: list[Attachment]
    subject: str
    text: str


class S3IServiceRequest(ReplyableMessage):
    """S³I service request model.

    Attributes:
        messageType (Literal["serviceRequest"]): Type of the message.
        serviceType (str): Type of service requested.
        parameters (dict): Parameters for the service.
    """

    messageType: Literal["serviceRequest"] = "serviceRequest"
    serviceType: str
    parameters: dict


class S3IServiceReply(ReplyMessage):
    """S³I service reply model.

    Attributes:
        messageType (Literal["serviceReply"]): Type of the message.
        serviceType (str): Type of service.
        result (Any): Result of the service.
    """

    messageType: Literal["serviceReply"] = "serviceReply"
    serviceType: str
    results: Any


class S3IGetValueRequest(AttributeMessage):
    """S³I get value request model.

    Attributes:
        messageType (Literal["getValueRequest"]): Type of the message.
    """

    messageType: Literal["getValueRequest"] = "getValueRequest"


class S3IGetValueReply(ReplyMessage):
    """S³I get value reply model.

    Attributes:
        messageType (Literal["getValueReply"]): Type of the message.
        value (Any): Retrieved value.
    """

    messageType: Literal["getValueReply"] = "getValueReply"
    value: Any


class S3ISetValueRequest(AttributeMessage):
    """S³I set value request model.

    Attributes:
        messageType (Literal["setValueRequest"]): Type of the message.
        newValue (Any): New value to set.
    """

    messageType: Literal["setValueRequest"] = "setValueRequest"
    newValue: Any


class S3ISetValueReply(ReplyMessage):
    """S³I set value reply model.

    Attributes:
        messageType (Literal["setValueReply"]): Type of the message.
    """

    messageType: Literal["setValueReply"] = "setValueReply"


class S3ICreateAttributeRequest(AttributeMessage):
    """S³I create attribute request model.

    Attributes:
        messageType (Literal["createAttributeRequest"]): Type of the message.
        newValue (str): Value of the new attribute.
    """

    messageType: Literal["createAttributeRequest"] = "createAttributeRequest"
    newValue: str


class S3ICreateAttributeReply(ReplyMessage):
    """S³I create attribute reply model.

    Attributes:
        messageType (Literal["createAttributeReply"]): Type of the message.
        replyingToMessage (str): Identifier of the referenced message.
        ok (bool): Status of the operation.
    """

    messageType: Literal["createAttributeReply"] = "createAttributeReply"
    replyingToMessage: str
    ok: bool


class S3IDeleteAttributeRequest(AttributeMessage):
    """S³I delete attribute request model.

    Attributes:
        messageType (Literal["deleteAttributeRequest"]): Type of the message.
    """

    messageType: Literal["deleteAttributeRequest"] = "deleteAttributeRequest"


class S3IDeleteAttributeReply(ReplyMessage):
    """S³I delete attribute reply model.

    Attributes:
        messageType (Literal["deleteAttributeReply"]): Type of the message.
        ok (bool): Status of the operation.
    """

    messageType: Literal["deleteAttributeReply"] = "deleteAttributeReply"
    ok: bool


S3IMessageTypes = Annotated[
    Union[
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
    ],
    Field(discriminator="messageType"),
]

S3IMessage: TypeAdapter[S3IMessageTypes] = TypeAdapter(S3IMessageTypes)


class S3IEvent(BaseModel):
    """S³I event model.

    Attributes:
        sender (str): Identifier of the sender.
        identifier (str): Unique identifier for this event.
        timestamp (int): Unix timestamp of the event.
        topic (str): Topic associated with the event.
        messageType (Literal["event"]): Type of the message.
        content (ContentType): Event content with a default type of dict.
    """

    sender: str
    identifier: str
    timestamp: int
    topic: str
    messageType: Literal["event"] = "event"
    content: Any
