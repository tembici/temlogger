from .base import FormatterBase


class StackDriverFormatter(FormatterBase):

    def format(self, record):
        message = super().format(record)
        return message
