from functools import wraps
from flask import abort
from flask_login import current_user, login_required

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if not current_user.can(permission, current_user.curr_conf):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# def admin_required(f):
#     # print func
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if not current_user.is_authenticated:
#                 abort(403)
#             if not current_user.is_administrator():
#                 abort(403)
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

def chair_required(f):
    return permission_required(Permission.MANAGE_CONFERENCE)(f)


def admin_required(f):
    return permission_required(0xff)(f)
