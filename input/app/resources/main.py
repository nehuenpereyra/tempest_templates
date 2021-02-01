
from flask import redirect, url_for

from app.helpers.login import authenticated


def index():
    if authenticated():
        return redirect(url_for("user_index"))
    else:
        return redirect(url_for("auth_login"))
