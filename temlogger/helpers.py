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
