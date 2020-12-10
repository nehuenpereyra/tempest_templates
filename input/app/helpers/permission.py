from flask import abort
# from flask_login import current_user


# def flatten(l): return [item for sublist in l for item in sublist]


# def verify_permission(permission):
#     for user_permission in set(flatten(list(map(lambda each: each.permissions, current_user.roles)))):
#         if(user_permission.name == permission):
#             return True
#     return False


# def permission(name):
#     def wrapper_1(function):
#         def wrapper_2(*args, **kwargs):
#             if not verify_permission(name):
#                 abort(403)
#             return function(*args, **kwargs)
#         return wrapper_2
#     return wrapper_1

def verify_permission(permission):
    return True


def permission(name):
    def wrapper_1(function):
        def wrapper_2(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper_2
    return wrapper_1
