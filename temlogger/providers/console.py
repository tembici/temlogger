from .base import FormatterBase


class ConsoleFormatter(FormatterBase):

    def format(self, record):
        message = super().format(record)
        return self.serialize(message)
