from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, login_user, current_user
import datetime, hashlib

from accounts.forms import RegisterForm, LoginForm, UpdataForm, SuperForm, ResetForm, ResetPasswordForm
from model import User, db, TotalOrder, Order

accounts = Blueprint('accounts', __name__,
                     template_folder="templates",
                     static_folder="static")


@accounts.route("/login", methods = ["GET", "POST"])
def login():
    registerform = RegisterForm()
    loginform = LoginForm()

    if registerform.register.data and registerform.validate_on_submit():
        username = registerform.username.data
        password = registerform.password.data
        email = registerform.email.data
        phone = registerform.phone.data
        birth = registerform.birth.data

        pw_hash = hashlib.sha256(password.encode()).hexdigest()

        user = User(username=username,
                    password=pw_hash,
                    email=email,
                    phone=phone,
                    birth=birth)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully, Please login")
        return redirect(url_for("accounts.login"))

    if loginform.login.data and loginform.validate_on_submit():
        username = loginform.loginusername.data
        password = loginform.loginpassword.data
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter(User.username == username, User.deleted_at == None).first()
        if user.password == pw_hash:
            login_user(user)
            return redirect(url_for("shop.index"))
        else:
            flash("Username or Password Wrong")
    return render_template("login.html", registerform=registerform, loginform=loginform)


@accounts.route("/verify_mail", methods=["GET", "POST"])
def verify_mail():
    resetform = ResetForm()

    if resetform.validate_on_submit():
        email = resetform.email.data
        user = User.query.filter(User.email == email, User.deleted_at == None).first()
        if user:
            reset_password_id = hashlib.sha256(str(user.id).encode()).hexdigest()
            return redirect(url_for("accounts.reset", id=reset_password_id))
        flash("Without this EMAIL")

    return render_template("resrt_verify_mail.html", resetform=resetform)


@accounts.route("/reset/<id>", methods=["GET", "POST"])
def reset(id):
    resetpasswordform = ResetPasswordForm()

    if resetpasswordform.validate_on_submit():
        email = resetpasswordform.email.data
        password = resetpasswordform.password.data
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter(User.email == email, User.deleted_at == None).first()
        user.password = pw_hash
        db.session.commit()
        return redirect(url_for("accounts.login"))
    return render_template("reset_password.html", resetpasswordform=resetpasswordform)


@accounts.route("/user", methods=["GET", "POST"])
@login_required
def user():
    updataform = UpdataForm()

    email_value = current_user.email
    phone_value = current_user.phone
    birth_value = current_user.birth

    if updataform.validate_on_submit():
        password = updataform.password.data
        email = updataform.email.data
        phone = updataform.phone.data
        birth = updataform.birth.data

        User.query.filter(User.id == current_user.id).update(
            dict(password=password,
                 email=email,
                 phone=phone,
                 birth=birth))
        db.session.commit()
        flash("Successfully updated")
        return redirect(url_for("accounts.user"))
    return render_template("user.html",
                           updataform=updataform,
                           email_value=email_value,
                           phone_value=phone_value,
                           birth_value=birth_value)


@accounts.route("/order", methods=["GET", "POST"])
@login_required
def order():
    totalorders = TotalOrder.query.filter_by(user_id=current_user.id).order_by(TotalOrder.id.desc()).all()
    if request.form.get("det"):
        totalorders_id = request.form.get("det")
        return redirect(url_for("accounts.orderdetail", id=totalorders_id))

    return render_template("order.html", totalorders=totalorders)


@accounts.route("/orderdetail/<id>", methods=["GET", "POST"])
def orderdetail(id):
    orders = Order.query.filter_by(user_id=current_user.id, total_order_id=id).all()

    return render_template("orderdetail.html", orders=orders)


@accounts.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("accounts.login"))


@accounts.route("/management", methods=["GET", "POST"])
def management():
    users = User.query.all()

    if request.form.get("mod"):
        user_id = request.form.get("mod")
        return redirect(url_for("accounts.super", id=user_id))

    if request.form.get("del"):
        user_id = request.form.get("del")
        user = User.query.get(user_id)
        user.deleted_at = datetime.datetime.now()
        db.session.commit()
        return redirect(url_for("accounts.management"))

    return render_template("user_management.html", users=users)


@accounts.route("/super/<id>", methods=["GET", "POST"])
def super(id):
    superform = SuperForm()
    user = User.query.get(id)
    if superform.validate_on_submit():
        is_super = superform.is_super.data
        user.is_super = is_super
        db.session.commit()
        return redirect(url_for("accounts.management"))
    return render_template("user_super.html", superform=superform, user=user)


@accounts.route("/aboutus", methods=["GET", "POST"])
def aboutus():

    return render_template("aboutus.html")