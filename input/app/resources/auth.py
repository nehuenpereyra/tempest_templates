
from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user

from app.models import User
from app.helpers.login import authenticated
from app.helpers.forms import LoginForm


def login():
    if authenticated():
        return redirect(url_for("index"))
    return render_template("auth/login.html", form=LoginForm())


def authenticate():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("index"))
    return render_template("auth/login.html", form=form, authError=True)


def logout():
    logout_user()
    return redirect(url_for("index"))
