from exp_coord.handlers.new_image import NewImageHandler
from exp_coord.handlers.save_all import SaveAllEventsHandler, SaveAllMessagesHandler
from exp_coord.handlers.status import StatusHandler

EVENT_HANDLERS = [NewImageHandler, StatusHandler, SaveAllEventsHandler]
MESSAGE_HANDLERS = [SaveAllMessagesHandler]
