from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_uploads import secure_filename
import os, uuid, datetime
from flask_login import current_user, login_required

from shop.forms import ProductForm, ProductBuyForm, BuyForm, StatusForm
from model import db, Product, ProductImg, Order, TotalOrder


shop = Blueprint('shop',
                 __name__,
                 template_folder="templates",
                 static_folder="static")

path = "\static\image_fold"
paths = "D:\Code\shop\static\image_fold"


@shop.route("/index", methods = ["GET", "POST"])
def index():
    products = Product.query.filter(Product.deleted_at == None).order_by(
        Product.count.desc()).limit(9).all()

    return render_template("index.html", products=products)


@shop.route("/sports", methods=["GET", "POST"])
def sports():
    products = Product.query.filter(Product.classify=="Sports", Product.deleted_at==None, Product.count > 0).all()

    return render_template("class_sports.html", products=products)


@shop.route("/smart", methods=["GET", "POST"])
def smart():
    products = Product.query.filter(Product.classify=="Smart", Product.deleted_at==None, Product.count > 0).all()

    return render_template("class_smart.html", products=products)


@shop.route("/classic", methods=["GET", "POST"])
def classic():
    products = Product.query.filter(Product.classify=="Classic", Product.deleted_at==None, Product.count > 0).all()

    return render_template("class_classic.html", products=products)


@shop.route("/other", methods=["GET", "POST"])
def other():
    products = Product.query.filter(Product.classify=="Other", Product.deleted_at==None, Product.count > 0).all()

    return render_template("class_other.html", products=products)


@shop.route("/all", methods=["GET", "POST"])
def all():
    products = Product.query.filter(Product.deleted_at==None, Product.count > 0).all()

    return render_template("class_all.html", products=products)


@shop.route("/products/<id>", methods=["GET", "POST"])
def products(id):
    productbuyform = ProductBuyForm()
    product = Product.query.get(id)

    if productbuyform.validate_on_submit():
        if current_user.is_authenticated:
            order = Order.query.filter_by(product_id=id, user_id=current_user.id, deleted_at=None).first()
            if order:
                order.count = productbuyform.count.data + order.count
                order.price = (product.price * productbuyform.count.data) + order.price
                db.session.commit()
            else:
                count = productbuyform.count.data
                price = product.price * count
                order = Order(price=price, count=count, product_id=id, user_id=current_user.id)
                db.session.add(order)
                db.session.commit()
            flash("Add to Cart")
        else :
            flash("Please login first")
            return redirect(url_for("accounts.login"))
    return render_template("products.html", productbuyform=productbuyform, product=product)


@shop.route("/upload", methods=["GET", "POST"])
def upload():
    productform = ProductForm()
    if productform.validate_on_submit():
        name = productform.name.data
        content = productform.content.data
        price = productform.price.data
        count = productform.count.data
        classify = productform.classify.data

        product = Product(name=name,
                          content=content,
                          price=price,
                          count=count,
                          classify=classify)

        for img in productform.img.data:
            img_name = secure_filename(img.filename)
            print(img_name)
            ext = img_name.split('.', 1)[-1]
            new_imgname = uuid.uuid4().hex + '.' + ext
            img_save = os.path.join(paths, new_imgname)
            img.save(img_save)
            img_url = os.path.join(path, new_imgname)
            productimg = ProductImg(url=img_url)
            product.db_product_productimg.append(productimg)

        db.session.add(product)
        db.session.commit()
        flash("Uploaded Successfully")
        return redirect(url_for("shop.upload"))
    return render_template("upload.html", productform=productform)


@shop.route("/upload_modify/<id>", methods=["GET", "POST"])
def upload_modify(id):
    productform = ProductForm()
    product = Product.query.get(id)
    #productform.content.data = product.content
    #productform.classify.data = product.classify

    if request.form.get("del"):
        checks = request.form.getlist("check")
        for check in checks:
            img_id = ProductImg.query.get(check)
            img_id.deleted_at = datetime.datetime.now()
        db.session.commit()

    if productform.validate_on_submit():
        name = productform.name.data
        content = productform.content.data
        price = productform.price.data
        count = productform.count.data
        classify = productform.classify.data

        product.name = name
        product.content = content
        product.price = price
        product.count = count
        product.classify = classify

        for img in productform.modifyimg.data:
            img_name = secure_filename(img.filename)
            if img_name != "":
                ext = img_name.split('.', 1)[-1]
                new_imgname = uuid.uuid4().hex + '.' + ext
                img_save = os.path.join(paths, new_imgname)
                img.save(img_save)
                img_url = os.path.join(path, new_imgname)
                productimg = ProductImg(url=img_url)
                product.db_product_productimg.append(productimg)

        imgcount = ProductImg.query.filter(ProductImg.deleted_at == None, ProductImg.product_id == id).count()
        if imgcount > 0:
            db.session.add(product)
            db.session.commit()
            return redirect(url_for("shop.management"))
        else:
            flash("Product has no picture")
    return render_template("upload_modify.html", productform=productform, product=product)


@shop.route("/management", methods=["GET", "POST"])
@shop.route("/management/<int:page>", methods=["GET", "POST"])
def management(page=1):
    products = Product.query.filter_by(deleted_at=None).order_by(
        Product.id.desc()).paginate(page, 8, False)
    if request.form.get("ser"):
        num = request.form.get("serip_id")
        if num:
            num = int(num) - 1000000
            return redirect(url_for("shop.management_search", id=num))

    if request.form.get("add"):
        return redirect(url_for("shop.upload"))

    if request.form.get("mod"):
        product_id = request.form.get("mod")
        return redirect(url_for("shop.upload_modify", id=product_id))

    if request.form.get("del"):
        product_id = request.form.get("del")
        product = Product.query.get(product_id)
        product.deleted_at = datetime.datetime.now()

        for img in product.db_product_productimg:
            img.deleted_at = datetime.datetime.now()

        orders = Order.query.filter_by(deleted_at=None, product_id=product_id).all()
        for order in orders:
            order.deleted_at = datetime.datetime.now()

        db.session.commit()
        return redirect(url_for("shop.management"))

    return render_template("Product_management.html", products=products)


@shop.route("/management_search/<id>", methods=["GET", "POST"])
@shop.route("/management_search/<id>/<int:page>", methods=["GET", "POST"])
def management_search(id, page=1):
    products = Product.query.filter_by(deleted_at=None, id=id).order_by(
        Product.id.desc()).paginate(page, 8, False)

    if request.form.get("add"):
        return redirect(url_for("shop.upload"))

    if request.form.get("mod"):
        product_id = request.form.get("mod")
        return redirect(url_for("shop.upload_modify", id=product_id))

    if request.form.get("del"):
        product_id = request.form.get("del")
        product = Product.query.get(product_id)
        product.deleted_at = datetime.datetime.now()

        for img in product.db_product_productimg:
            img.deleted_at = datetime.datetime.now()

        orders = Order.query.filter_by(deleted_at=None,
                                       product_id=product_id).all()
        for order in orders:
            order.deleted_at = datetime.datetime.now()

        db.session.commit()
        return redirect(url_for("shop.management"))

    return render_template("Product_management_search.html", products=products)


@shop.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    orders = Order.query.filter(Order.user_id == current_user.id, Order.deleted_at == None).all()
    total_price = 0
    for order in orders:
        order.price = order.count * order.product.price
        if order.product.count <= 0:
            order.deleted_at = datetime.datetime.now()
        if order.count > order.product.count:
            order.count = order.product.count
            order.price = order.product.price * order.count
        db.session.commit()

    orders = Order.query.filter(Order.user_id == current_user.id, Order.deleted_at == None).all()

    for order in orders:
        total_price += order.price

    if request.form.get("del"):
        order_id = request.form.get("del")
        order = Order.query.filter_by(id=order_id).first()
        order.deleted_at = datetime.datetime.now()
        db.session.commit()
        return redirect(url_for("shop.cart"))

    if request.form.get("save"):
        count = request.form.get("save")
        order_id = request.form.get("savebu")
        order = Order.query.filter_by(id=order_id).first()
        product_price = order.product.price
        price = product_price * int(count)
        order.count = count
        order.price = price
        db.session.commit()
        return redirect(url_for("shop.cart"))

    if request.form.get("buy"):
        if len(orders) == 0:
            flash("Cart is empty")
        else:
            return redirect(url_for("shop.checkout"))
    return render_template("cart.html", orders=orders, total_price=total_price)


@shop.route("/checkout", methods=["GET", "POST"])
def checkout():
    buyform = BuyForm()
    orders = Order.query.filter_by(user_id=current_user.id, deleted_at=None).all()

    total_price = 0
    total_count = 0

    for order in orders:
        total_price += order.price
        total_count += order.count

    if buyform.validate_on_submit():
        for order in orders:
            order.product.count -= order.count
            if order.product.count < 0:
                flash("The remaining product quantity has changed, please reconfirm")
                return redirect(url_for("shop.cart"))
        name = buyform.name.data
        address = buyform.address.data
        phone = buyform.phone.data
        status = "Pending Payment"
        totalorder = TotalOrder(name=name,
                                address=address,
                                phone=phone,
                                user_id=current_user.id,
                                total_price=total_price,
                                total_count=total_count,
                                status=status)
        db.session.add(totalorder)
        db.session.commit()
        for order in orders:
            order.total_order_id = totalorder.id
            order.deleted_at = datetime.datetime.now()
            order.product.count -= order.count
        db.session.commit()
        return redirect(url_for("accounts.order"))

    return render_template("checkout.html",
                           buyform=buyform,
                           total_price=total_price,
                           total_count=total_count)


@shop.route("/total_order", methods=["GET", "POST"])
@shop.route("/total_order/<int:page>/", methods=["GET", "POST"])
def total_order(page=1):
    totalorders = TotalOrder.query.order_by(TotalOrder.id.desc()).paginate(
        page, 10, False)

    if request.form.get("ser"):
        num = request.form.get("serip_id")
        if num:
            num = int(num) - 1000000
            return redirect(url_for("shop.total_order_search", id=num))

    if request.form.get("det"):
        totalorders_id = request.form.get("det")
        return redirect(url_for("shop.total_order_modify", id=totalorders_id))
    return render_template("total_order.html", totalorders=totalorders)


@shop.route("/total_order_search/<id>", methods=["GET", "POST"])
@shop.route("/total_order_search/<id>/<int:page>/", methods=["GET", "POST"])
def allorder_search(id, page=1):
    totalorders = TotalOrder.query.filter_by(id=id).order_by(
        TotalOrder.id.desc()).paginate(page, 10, False)
    if request.form.get("det"):
        totalorders_id = request.form.get("det")
        return redirect(url_for("shop.total_order_modify", id=totalorders_id))
    return render_template("total_order_search.html", totalorders=totalorders)


@shop.route("/total_order_modify/<id>", methods=["GET", "POST"])
def total_order_modify(id):
    orders = Order.query.filter_by(total_order_id=id).all()
    totalorder = TotalOrder.query.get(id)
    statusform = StatusForm()
    if statusform.validate_on_submit():
        status = statusform.status.data
        totalorder_id = TotalOrder.query.get(id)
        totalorder_id.status = status
        db.session.commit()
        return redirect(url_for("shop.total_order"))
    return render_template("total_order_modify.html", orders=orders,
                           statusform=statusform, totalorder=totalorder)
