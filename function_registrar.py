
def _create_registrar():
    registry = {}

    def registrar(description, keywords):
        def wrapper(func):
            registry[func.__name__] = {"function": func, "description": description, "keywords": keywords}
            return func
        return wrapper
    registrar.all = registry
    return registrar


procurable = _create_registrar()


def get_methods(human_readable=True):
    if human_readable:
        return [method.replace("_", " ") for method in procurable.all]
    else:
        return procurable.all