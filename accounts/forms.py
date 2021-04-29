from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Regexp, Email
from utils.validators import validate_phone, validate_birth, validate_username, validate_loginusername, validate_email


class RegisterForm(FlaskForm):
    username = StringField(render_kw={
        "class": "loginip", "placeholder": " Username", "required": "required"
        }, validators=[Length(min=5,max=20,message="Username Length 5 ~ 20"),validate_username])

    password = PasswordField(render_kw={
        "class": "loginip", "placeholder": " Password", "required": "required"
        }, validators=[Length(min=5, max=20, message="Password Length 5 ~ 20")])

    confirm_password = PasswordField(render_kw={
            "class": "loginip", "placeholder": " Confirm Password", "required": "required"
        }, validators=[EqualTo("password", message="Password does not match")])

    email = StringField(render_kw={
        "class": "loginip", "placeholder": " E-mail", "required": "required"
        }, validators=[Email(), validate_email])

    phone = StringField(render_kw={
        "class": "loginip", "placeholder": " Phone", "required": "required"
        }, validators=[validate_phone])

    birth = DateField(render_kw={
        "class": "loginip", "placeholder": " Birth", "required": "required"
        }, validators=[validate_birth])

    register = SubmitField(render_kw={
        "class": "loginbu", "placeholder": "Register"})


class LoginForm(FlaskForm):
    loginusername = StringField(render_kw={
        "class": "loginip", "placeholder": " Username", "required": "required"
    }, validators=[Length(min=5, max=20, message="Username Length 5 ~ 20"),
       validate_loginusername
    ])

    loginpassword = PasswordField(render_kw={
        "class": "loginip", "placeholder": " Password", "required": "required"
        }, validators=[Length(min=5, max=20, message="Password Length 5 ~ 20")
    ])

    login = SubmitField(render_kw={
        "class": "loginbu", "placeholder": "Login"})


class UpdataForm(FlaskForm):
    password = PasswordField(render_kw={
        "class": "ip", "placeholder": " Password", "required": "required"
        }, validators=[Length(min=5, max=20, message="Password Length 5 ~ 20")])

    confirm_password = PasswordField(render_kw={
            "class": "ip", "placeholder": " Confirm Password", "required": "required"
        }, validators=[EqualTo("password", message="Password does not match")])

    email = StringField(render_kw={
        "class": "ip", "placeholder": " E-mail", "required": "required"
        }, validators=[Email()])

    phone = StringField(render_kw={
        "class": "ip", "placeholder": " Phone", "required": "required", "value": ""
        }, validators=[validate_phone])

    birth = DateField(render_kw={
        "class": "ip", "placeholder": " Birth", "required": "required"
        }, validators=[validate_birth])

    enter = SubmitField("Update",render_kw={
        "class": "bu", "placeholder": "Update"})


class SuperForm(FlaskForm):
    enter = SubmitField("Updata",render_kw={
        "class": "bu", "placeholder": "Updata"})

    is_super = SelectField("Super", render_kw={
        "class": "ip", "placeholder": " Super", "required": "required"
    }, choices=[(1, "No"),(2, "Super")], coerce=int)


class ResetForm(FlaskForm):
    email = StringField(render_kw={
        "class": "loginip", "placeholder": " E-mail", "required": "required"
        }, validators=[Email()])

    enter = SubmitField("Enter",render_kw={
        "class": "loginbu", "placeholder": "Enter"})


class ResetPasswordForm(FlaskForm):
    email = StringField(render_kw={
        "class": "loginip", "placeholder": " E-mail", "required": "required"
        }, validators=[Email()])
        
    password = PasswordField(render_kw={
        "class": "loginip", "placeholder": " Password", "required": "required"
        }, validators=[Length(min=5, max=20, message="Password Length 5 ~ 20")])

    confirm_password = PasswordField(render_kw={
            "class": "loginip", "placeholder": " Confirm Password", "required": "required"
        }, validators=[EqualTo("password", message="Password does not match")])

    enter = SubmitField("Enter",render_kw={
        "class": "loginbu", "placeholder": "Enter"})