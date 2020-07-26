
def _create_procurable_registrar():
    registry = {}

    def registrar(description, keywords):
        def wrapper(func):
            registry[func.__name__] = {"function": func, "description": description, "keywords": keywords}
            return func
        return wrapper
    registrar.all = registry
    return registrar


def _create_selectable_registrar():
    registry = {}

    def registrar(description):
        def wrapper(func):
            registry[func.__name__] = {"function": func, "description": description, "endpoint": func.__name__}
            return func
        return wrapper
    registrar.all = registry
    return registrar


procurable = _create_procurable_registrar()
selectable = _create_selectable_registrar()


def get_procurable(human_readable=True):
    if human_readable:
        return [method.replace("_", " ") for method in procurable.all]
    else:
        return procurable.all


def get_selectable(human_readable=True):
    if human_readable:
        return [method.replace("_", " ") for method in selectable.all]
    else:
        return selectable.all