import itertools

from logstash.formatter import LogstashFormatterBase
from temlogger import config

from ..helpers import import_string_list


class FormatterBase(LogstashFormatterBase):

    def __init__(self, fqdn=False, app_name='', environment='',
                 event_handlers=[], *args, **kwargs):
        super().__init__(message_type='', fqdn=fqdn, *args, **kwargs)
        self.app_name = app_name
        self.environment = environment
        self.event_handlers = import_string_list(event_handlers)

    def format_with_handlers(self, message):
        default_handlers = config.get_event_handlers()
        handlers = itertools.chain(default_handlers, self.event_handlers)

        for handle in handlers:
            message = handle(message)

        return message

    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': self.format_timestamp(record.created),
            'message': record.getMessage(),
            'host': self.host,
            'path': record.pathname,
            'environment': self.environment,
            'app_name': self.app_name,

            # Extra Fields
            'level': record.levelname,
            'logger_name': record.name,
        }

        # Add extra fields
        payload_fields = self.get_extra_fields(record)
        message.update(payload=payload_fields)

        # If exception, add debug info
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        message = self.format_with_handlers(message)

        return message
