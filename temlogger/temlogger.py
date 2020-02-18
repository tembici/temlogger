import logging
import os


class LoggingProvider:
    STACK_DRIVER = 'stackdriver'
    LOGSTASH = 'logstash'
    DEFAULT = 'default'


class LoggingConfig:
    _provider = ''
    _url = ''
    _port = ''
    _environment = ''

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

    def clear(self):
        self._provider = ''
        self._url = ''
        self._port = ''
        self._environment = ''


class LoggerManager:

    def get_logger(self, name):
        logging_provider = config.get_provider()

        logger = logging.getLogger(name)
        has_log_provider = hasattr(logger, 'logging_provider')
        if has_log_provider and logger.logging_provider == logging_provider:
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
        import logstash
        from .formatter import LogstashFormatter

        logging_url = config.get_url()
        logging_port = config.get_port()
        logging_environment = config.get_environment()

        logger = logging.getLogger(name)
        logger.logging_provider = LoggingProvider.LOGSTASH

        logger.setLevel(logging.INFO)
        handler = logstash.TCPLogstashHandler(
            logging_url, logging_port, version=1)
        handler.setFormatter(LogstashFormatter(
            environment=logging_environment))
        logger.addHandler(handler)

        return logger

    def get_logger_stackdriver(self, name):
        """
        Docs: https://googleapis.dev/python/logging/latest/handlers.html
        """
        import google.cloud.logging
        from .formatter import StackDriverFormatter

        logging_environment = config.get_environment()

        logger = logging.getLogger(name)
        logger.logging_provider = LoggingProvider.STACK_DRIVER

        client = google.cloud.logging.Client()

        handler = client.get_default_handler()
        # Setup logger explicitly with this handler
        handler.setFormatter(StackDriverFormatter(
            environment=logging_environment))
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
