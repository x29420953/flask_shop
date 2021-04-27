from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, MultipleFileField, TextAreaField, SelectField
from wtforms.validators import ValidationError
from flask_wtf.file import FileAllowed, FileRequired, FileField

from utils.validators import validate_phone


class ProductForm(FlaskForm):
    name = StringField("Name", render_kw={
        "class": "ip", "placeholder": " Name", "required": "required"
    })

    content = TextAreaField("Content", render_kw={
        "class": "ipa", "placeholder": "Content", "required": "required"
    })

    price = IntegerField("Price", render_kw={
        "class": "ip", "placeholder": " Price", "required": "required"
    })

    count = IntegerField("Count", render_kw={
        "class": "ip", "placeholder": " Count", "required": "required"
    })

    classify = SelectField("Count", render_kw={
        "class": "ip", "placeholder": " Classify", "required": "required"
    }, choices=[("Sports", "Sports"), ("Smart", "Smart"), ("Classic", "Classic"), ("Other", "Other")])

    img = MultipleFileField("Img", render_kw={
        "class": "ip", "required": "required", "accept": ".jpg, .jpge, .png, .jfif"})

    modifyimg = MultipleFileField("Img", render_kw={
        "class": "ip", "accept": ".jpg, .jpge, .png, .jfif"})

    upload = SubmitField(render_kw={
        "class": "bu", "placeholder": "Upload"})



class ProductBuyForm(FlaskForm):
    count = IntegerField("Count", render_kw={
        "class": "ip1", "required": "required", "id":"count", "value":"1"
    })

    addcart = SubmitField(render_kw={
        "class": "bu", "placeholder": "Add Cart"})


class BuyForm(FlaskForm):
    name = StringField("Name", render_kw={
        "class": "ip", "placeholder": " Name", "required": "required"
    })

    address = StringField("Address", render_kw={
        "class": "ip", "placeholder": " Address", "required": "required"
    })

    phone = StringField("Phone", render_kw={
        "class": "ip", "placeholder": " Phone", "required": "required"
    }, validators=[validate_phone])

    buy = SubmitField("Complete Purchase", render_kw={"class": "bu"})


class StatusForm(FlaskForm):
    status = SelectField("Status", render_kw={"class": "ip", "placeholder": " Status"
    }, choices=[("Pending Payment", "Pending Payment"),
                ("Shipment Processing", "Shipment Processing"),
                ("Shipped", "Shipped"),
                ("Complete", "Complete")])

    enter = SubmitField("Enter", render_kw={"class": "bu"})