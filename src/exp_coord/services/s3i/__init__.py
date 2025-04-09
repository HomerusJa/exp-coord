from typing import TypeAlias

from .base import Handler as Handler
from .base import Processor as Processor
from .base import S3IError as S3IError
from .broker import S3IBrokerClient as S3IBrokerClient
from .broker import S3IEvent as S3IEvent
from .broker import S3IMessage as S3IMessage

EventHandler: TypeAlias = Handler[S3IEvent]
EventProcessor: TypeAlias = Processor[S3IEvent]

MessageHandler: TypeAlias = Handler[S3IMessage]
MessageProcessor: TypeAlias = Processor[S3IMessage]
