import string
import random

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
# 用于对明文密码加密
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # 在 cookie 存储登陆授权信息
                # flask 中的 session 是经过加密后存储在 cookie 中的
                session['user_id'] = user.id
                return redirect('/')
            else:
                print("密码错误！")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


# GET：从服务器上读取数据
# POST：将客户端数据交给服务器
@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱或验证码是否对应且正确
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # 实现向登陆页面的跳转
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route('/captcha')
def send_captcha():
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    email = request.args.get("email")
    message = Message(subject="验证码", recipients=[email], body=captcha)
    mail.send(message)
    # 将邮箱和验证码存入数据库
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '验证码发送成功'})

@bp.route('logout')
def logout():
    session.clear()
    return redirect("/")

@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["18186126127@163.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"
