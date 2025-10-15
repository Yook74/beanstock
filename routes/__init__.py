from functools import wraps

from werkzeug.exceptions import NotFound

def by_id(model_class):
    def decorator(route):
        @wraps(route)
        def wrapper(id):
            row = model_class.query.filter_by(id=id).first()
            if row is None:
                raise NotFound(f'No {model_class.__name__} found with the given ID')

            return route(row)
        return wrapper
    return decorator

from . import root, item

blueprints = [root.bluep, item.bluep]
