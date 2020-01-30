import logging
import logstash
import os

from .formatter import StackDriverFormatter


class LoggingProvider:
    STACK_DRIVER = 'stackdriver'
    LOGSTASH = 'logstash'
    DEFAULT = 'default'


class LoggingConfig:
    _logging_provider = ''
    _logging_url = ''
    _logging_port = ''

    def set_logging_provider(self, value):
        self._logging_provider = value

    def get_logging_provider(self):
        return self._logging_provider.lower() or os.getenv('LOGGING_PROVIDER', '').lower()

    def set_logging_url(self, value):
        self._logging_url = value

    def get_logging_url(self):
        return self._logging_url or os.getenv('LOGGING_URL', '')

    def set_logging_port(self, value):
        self._logging_port = value

    def get_logging_port(self):
        return self._logging_port or os.getenv('LOGGING_PORT', '')

    def clear(self):
        self._logging_provider = ''
        self._logging_url = ''
        self._logging_port = ''


class LoggerManager:

    def get_logger(self, name):
        logging_provider = config.get_logging_provider()

        logger = logging.getLogger(name)
        if hasattr(logger, 'logging_provider') and logger.logging_provider == logging_provider:
            return logger

        logger.handlers.clear()

        if logging_provider == LoggingProvider.LOGSTASH:
            return self.get_logger_logstash(name)
        elif logging_provider == LoggingProvider.STACK_DRIVER:
            return self.get_logger_stackdriver(name)
        return self.get_logger_default(name)

    def get_logger_default(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.logging_provider = LoggingProvider.DEFAULT

        return logger

    def get_logger_logstash(self, name):
        loggin_url = config.get_logging_url()
        logging_port = config.get_logging_port()

        logger = logging.getLogger(name)
        logger.logging_provider = LoggingProvider.LOGSTASH

        logger.setLevel(logging.INFO)
        logger.addHandler(
            logstash.TCPLogstashHandler(
                loggin_url, logging_port, version=1))

        return logger

    def get_logger_stackdriver(self, name):
        """
        Docs: https://googleapis.dev/python/logging/latest/handlers.html
        """
        import google.cloud.logging

        logger = logging.getLogger(name)
        logger.logging_provider = LoggingProvider.STACK_DRIVER

        client = google.cloud.logging.Client()

        handler = client.get_default_handler()
        # Setup logger explicitly with this handler
        handler.setFormatter(StackDriverFormatter())
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger


config = LoggingConfig()
logger_manager = LoggerManager()


def getLogger(name: str):
    return logger_manager.get_logger(name)


__all__ = [
    'getLogger',
    'config',
]
