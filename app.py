from flask import Flask, render_template, request, jsonify, session, abort, redirect, url_for, Response
from flask_mail import Mail, Message
from pymongo import MongoClient
import datetime
import re
import os
import random
import json
import urllib.parse
import urllib.request
import hashlib

app = Flask(__name__)
app.secret_key = b'\xc0:8!E<\x96\xe8\xff\x0b\xd5\xff\x15\xf4m\xb0<\x9b\xc5]\xd5\x03X6'

app.config.update(
    DEBUG=False,
    MAIL_SERVER='smtp-relay.brevo.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=('admin', 'xxxxxx@gmail.com'),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME='yoni980807@gmail.com',
    MAIL_PASSWORD='xxxxxxxxx'
)

mail = Mail(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["message"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reg", methods=["GET", "POST"])
def reg_handle():
    if request.method == "GET":
        return render_template("reg.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        upass = request.form.get("upass")
        upass2 = request.form.get("upass2")
        verify_code = request.form.get("verify_code")
        email = request.form.get("email")

        if not (uname and uname.strip() and upass and upass2 and verify_code and email):
            abort(500)

        if re.search(r"[\u4E00-\u9FFF]", uname):
            abort(Response("中文名稱請使用英文名稱！"))

        if not re.fullmatch("[a-zA-Z0-9_]{4,20}", uname):
            abort(Response("帳號名稱請介於4-20個字，且僅接受英文、數字、和底線"))

        cur = db.mb_user.find_one({"uname": uname})
        if cur:
            abort(Response("帳號已被註冊！"))

        if not (len(upass) >= 6 and len(upass) <= 15 and upass == upass2):
            abort(Response("密碼錯誤！"))

        if not re.fullmatch(r"[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+", email):
            abort(Response("信箱格式錯誤！"))

        try:
            db.mb_user.insert_one({
                "uname": uname,
                "upass": hashlib.md5(upass.encode()).hexdigest(),
                "email": email,
                "reg_time": datetime.datetime.now(),
                "last_login_time": datetime.datetime.now(),
                "priv": '1',
                "state": '1'
            })
        except:
            abort(Response("註冊失敗！"))

        return redirect(url_for("login_handle"))

@app.route("/user_center")
def user_center():
    user_info = session.get("user_info")

    if user_info:
        return render_template("user_center.html", uname=user_info.get("uname"))
    else:
        return redirect(url_for("login_handle"))

@app.route("/logout")
def logout_handle():
    res = {"err": 1, "desc": "請先登入！"}
    if session.get("user_info"):
        session.pop("user_info")
        res["err"] = 0
        res["desc"] = "登出成功！"
    return jsonify(res)

@app.route("/message_board", methods=["GET", "POST"])
def message_board_handle():
    if request.method == "GET":
        messages = db.mb_message.find()
        return render_template("message_board.html", messages=messages)
    elif request.method == "POST":
        user_info = session.get("user_info")
        if not user_info:
            abort(Response("請先登入！"))

        content = request.form.get("content")
        if content:
            content = content.strip()
            if 0 < len(content) <= 200:
                uid = user_info.get("uid")
                db.mb_message.insert_one({
                    "uid": uid,
                    "content": content,
                    "pub_time": datetime.datetime.now()
                })
                return redirect(url_for("message_board_handle"))
            else:
                abort(Response("留言內容長度需在1-200字之間！"))
        else:
            abort(Response("留言內容不能為空！"))

if __name__ == "__main__":
    app.run(port=8080, debug=True, host='0.0.0.0')