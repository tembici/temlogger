import os
import temlogger


path = os.path.dirname(__file__)
INVALID_GOOGLE_CREDENTIALS = os.path.join(path, 'resources/test_google_credentials_invalid.json')
VALID_GOOGLE_CREDENTIALS = os.path.join(path, 'resources/test_google_credentials.json')


def clean_temlogger_config():
    environments_to_clean = [
        'TEMLOGGER_PROVIDER',
        'TEMLOGGER_URL',
        'TEMLOGGER_PORT'
        'TEMLOGGER_ENVIRONMENT',
        'TEMLOGGER_LOG_LEVEL',
        'TEMLOGGER_APP_NAME',
    ]
    for env in environments_to_clean:
        if env in os.environ:
            del os.environ[env]

    temlogger.config.reset()


def add_tracker_id_to_message(message):
    message['tracker_id_global'] = 'tracker_id_value_global'
    return message
