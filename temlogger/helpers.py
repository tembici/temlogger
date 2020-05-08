import base64
import tempfile


from google.cloud.logging import Client as LoggingClient
from importlib import import_module


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" %
                          dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err


def import_string_list(dotted_path_list=[]):
    """
       dotted_path_list can be a list of dotted strings or
       mixed dotted strings and modules
    """
    module_list = []
    for handler in dotted_path_list:
        module = handler
        if not callable(handler):
            module = import_string(handler)

        module_list.append(module)
    return module_list


def load_google_client(base64_data, scopes=[]):
    if not base64_data:
        return ''

    decoded = base64.b64decode(base64_data).decode('utf-8')

    # From: https://github.com/googleapis/google-cloud-python/issues/7291#issuecomment-461135696
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(decoded.encode('ascii'))
        temp.flush()
        client = LoggingClient.from_service_account_json(temp.name)

    return client


def encode_file_as_base64(file_path):
    content_bin = open(file_path).read().encode('ascii')
    invalid_cred_base64 = base64.b64encode(content_bin).decode('utf-8')
    return invalid_cred_base64
