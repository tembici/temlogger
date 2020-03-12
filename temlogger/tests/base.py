import os
import temlogger


def clean_temlogger_config():
    environments_to_clean = [
        'TEMLOGGER_PROVIDER',
        'TEMLOGGER_URL',
        'TEMLOGGER_PORT'
        'TEMLOGGER_ENVIRONMENT'
    ]
    for env in environments_to_clean:
        if env in os.environ:
            del os.environ[env]

    temlogger.config.clear()


def add_tracker_id_to_message(message):
    message['tracker_id_global'] = 'tracker_id_value_global'
    return message
