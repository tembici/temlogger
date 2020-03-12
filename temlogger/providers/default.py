from .base import FormatterBase


class DefaultFormatter(FormatterBase):

    def format(self, record):
        message = super().format(record)
        return self.serialize(message)
