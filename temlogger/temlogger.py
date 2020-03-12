import logging
import os


from .helpers import import_string_list


class LoggingProvider:
    STACK_DRIVER = 'stackdriver'
    LOGSTASH = 'logstash'
    DEFAULT = 'default'


class LoggingConfig:
    _provider = ''
    _url = ''
    _port = ''
    _environment = ''
    _event_handlers = []

    def set_provider(self, value):
        self._provider = value

    def get_provider(self):
        return self._provider.lower() or os.getenv('TEMLOGGER_PROVIDER', '').lower()

    def set_url(self, value):
        self._url = value

    def get_url(self):
        return self._url or os.getenv('TEMLOGGER_URL', '')

    def set_port(self, value):
        self._port = value

    def get_port(self):
        return self._port or os.getenv('TEMLOGGER_PORT', '')

    def set_environment(self, value):
        self._environment = value

    def get_environment(self):
        return self._environment or os.getenv('TEMLOGGER_ENVIRONMENT', '')

    def get_event_handlers(self):
        return self._event_handlers

    def setup_event_handlers(self, event_handlers=[]):
        self._event_handlers = import_string_list(event_handlers)

    def clear(self):
        self._provider = ''
        self._url = ''
        self._port = ''
        self._environment = ''
        self._event_handlers = []


class LoggerManager:

    def __init__(self):
        self.logger_map = {
            LoggingProvider.LOGSTASH: self.get_logger_logstash,
            LoggingProvider.STACK_DRIVER: self.get_logger_stackdriver,
            LoggingProvider.DEFAULT: self.get_logger_default,
        }

    def get_logger(self, name, event_handlers=[]):
        logging_provider = config.get_provider()

        logger = logging.getLogger(name)
        has_log_provider = hasattr(logger, 'logging_provider')
        if has_log_provider and logger.logging_provider == logging_provider:
            return logger

        logger.handlers.clear()

        func = self.logger_map.get(logging_provider, self.get_logger_default)

        return func(name, event_handlers)

    def get_logger_default(self, name, event_handlers=[]):

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.logging_provider = LoggingProvider.DEFAULT

        return logger

    def get_logger_logstash(self, name, event_handlers=[]):
        from logstash import TCPLogstashHandler
        from .providers.logstash import LogstashFormatter

        logging_url = config.get_url()
        logging_port = config.get_port()
        logging_environment = config.get_environment()

        logger = logging.getLogger(name)
        logger.logging_provider = LoggingProvider.LOGSTASH

        logger.setLevel(logging.INFO)
        handler = TCPLogstashHandler(logging_url, logging_port, version=1)
        handler.setFormatter(LogstashFormatter(
            environment=logging_environment,
            event_handlers=event_handlers
        ))
        logger.addHandler(handler)

        return logger

    def get_logger_stackdriver(self, name, event_handlers=[]):
        """
        Docs: https://googleapis.dev/python/logging/latest/handlers.html
        """
        import google.cloud.logging
        from .providers.stackdriver import StackDriverFormatter

        logging_environment = config.get_environment()

        logger = logging.getLogger(name)
        logger.logging_provider = LoggingProvider.STACK_DRIVER

        client = google.cloud.logging.Client()

        handler = client.get_default_handler()

        # Setup logger explicitly with this handler
        handler.setFormatter(StackDriverFormatter(
            environment=logging_environment,
            event_handlers=event_handlers)
        )

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger


config = LoggingConfig()
logger_manager = LoggerManager()


def getLogger(name: str, event_handlers=[]):
    """Creates a logger with .

    :type name: str
    :param name: the name of the logger to be constructed.

    :type event_handlers: list
    :param name: list of event handlers

    :rtype: :class:`logging.Logger`
    :returns: Logger created.
    """
    return logger_manager.get_logger(name, event_handlers)


__all__ = [
    'getLogger',
    'config',
]
