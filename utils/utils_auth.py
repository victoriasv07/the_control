# from functools import wraps
# from flask_login import UserMixin, login_required, logout_user, LoginManager, login_user, current_user
# from flask import abort

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or not current_user.is_admin:
#             abort(403)  # Acesso negado se não for admin
#         return f(*args, **kwargs)
#     return decorated_function
