from logstash.formatter import LogstashFormatterBase


class FormatterBase(LogstashFormatterBase):

    def __init__(self, tags=None, fqdn=False, environment='', event_handlers=[],
                 *args, **kwargs):
        super().__init__(message_type='', tags=tags, fqdn=fqdn, *args, **kwargs)
        self.environment = environment
