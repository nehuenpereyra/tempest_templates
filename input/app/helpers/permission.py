from flask import abort
from flask_login import current_user


def flatten(l): return [item for sublist in l for item in sublist]


def verify_permission(permission):
    """Returns true if the currently logged in user has the permission.

    Keyword arguments:
    permission -- string representing permission
    """
    for user_permission in set(flatten(list(map(lambda each: each.permissions, current_user.roles)))):
        if(user_permission.name == permission):
            return True
    return False


def permission(name):
    """Decorator that verifies if the currently logged in user has the permissions to perform an operation.
    If you don't have the permissions, perform an abort (403).

    Keyword arguments:
    name -- string representing permission
    """
    def wrapper_1(function):
        def wrapper_2(*args, **kwargs):
            if not verify_permission(name):
                abort(403)
            return function(*args, **kwargs)
        return wrapper_2
    return wrapper_1
