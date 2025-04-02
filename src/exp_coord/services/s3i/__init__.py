from typing import TypeAlias

from exp_coord.services.s3i.base.processor import Handler as Handler
from exp_coord.services.s3i.base.processor import Processor as Processor
from exp_coord.services.s3i.broker.client import S3IBrokerClient as S3IBrokerClient
from exp_coord.services.s3i.broker.models import S3IEvent as S3IEvent
from exp_coord.services.s3i.broker.models import S3IMessage

EventHandler: TypeAlias = Handler[S3IEvent]
EventProcessor: TypeAlias = Processor[S3IEvent]

MessageHandler: TypeAlias = Handler[S3IMessage]
MessageProcessor: TypeAlias = Processor[S3IMessage]
