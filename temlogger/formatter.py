import logstash
from logstash.formatter import LogstashFormatterBase


class StackDriverFormatter(LogstashFormatterBase):

    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': self.format_timestamp(record.created),
            'message': record.getMessage(),
            'host': self.host,
            'path': record.pathname,
            'tags': self.tags,

            # Extra Fields
            'level': record.levelname,
            'logger_name': record.name,
        }

        # Add extra fields
        message.update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return message
