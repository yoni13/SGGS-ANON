from flask import Blueprint, abort, request, jsonify, current_app
from app import db
import time
import random
import re
from app import limiter
from flask_mail import Message
from app import mail

api = Blueprint('api', __name__)


@api.route('/api/v1/')
def index():
    return 'This is the sggs-anon API v1'

@api.route('/api/v1/mb_board/')
def mb_board():

    if request.args.get('limit'):
        if not request.args.get('limit').isdigit():
            return abort(400, 'limit must be a number')
        limit = request.args.get('limit')
    else:
        limit = 10

    if request.args.get('page'):
        if not request.args.get('page').isdigit():
            return abort(400, 'page must be a number')
        page = int(request.args.get('page'))
    else:
        page = 1


    datas = db.mb_message.find().sort({'_id':-1}).limit(limit).skip((page-1)*limit)
    res = []
    for data in datas:
        replys_count = db.mb_replys.count_documents({"post_id": data['post_id']})

        info = {'uname': data['uname'], 'content': data['content'], 'pub_time': data['pub_time'], 'post_id': data['post_id'], 'replys_count': replys_count}
        res.append(info)

    if request.args.get('reverse') == '1':
        res = list(res)
    else:
        res = list(reversed(res))
        
    return jsonify(res)

@api.route('/api/v1/mb_replys/')
def mb_board_post():
    post_id = request.args.get('post_id')
    if not post_id:
        return jsonify({"error": "post_id is required"}), 400

    if request.args.get('limit'):
        if not request.args.get('limit').isdigit():
            return jsonify({"error": "limit must be a number"}), 400
        
        limit = int(request.args.get('limit'))
    else:
        limit = 10

    if request.args.get('page'):
        if not request.args.get('page').isdigit():
            return jsonify({"error": "page must be a number"}), 400
        page = int(request.args.get('page'))
    else:
        page = 1

    data = db.mb_message.find_one({'post_id': post_id})
    if data:
        res = {'post':
               {'uname': data['uname'], 'content': data['content'], 'pub_time': data['pub_time'], 'post_id': data['post_id']}
                }
        replysres = []
        replys = db.mb_replys.find({'post_id': post_id}).limit(limit).skip((page-1)*limit)
        for reply in replys:
            replydata = {'uname': reply['uname'], 'content': reply['content'], 'pub_time': reply['pub_time']}
            replysres.append(replydata)
        res['replys'] = replysres
        if request.args.get('reverse') == '1':
            res['replys'] = list(reversed(res['replys']))
        return jsonify(res)
    else:
        return abort(400)
    
@api.route('/api/v1/send_email_code', methods=['POST'])
@limiter.limit("1/second")
def send_email_code():
    email = request.json.get('email')
    if not email:
        return jsonify({"err": 1, "desc": "請輸入信箱！"})

    if not re.fullmatch(r"[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+", email):
        return jsonify({"err": 1, "desc": "信箱格式錯誤！"})

    if db.mb_user.find_one({"email": email}):
        return jsonify({"err": 1, "desc": "信箱已被註冊！"})

    code = random.randint(100000, 999999)
    if db.reg_code.find_one({"email":email}):
        db.reg_code.delete_one({"email":email})
    db.reg_code.insert_one({
    "email":email,
    "reg_code":str(code),
    "send_time":time.time()
    })
    msg = Message('SGGS ANON 驗證碼', recipients=[email])
    msg.body = '您的驗證碼是：' + str(code) +'，有效期為5分鐘。'
    mail.send(msg)
    return jsonify({"err": 0, "desc": "驗證碼已發送！"})
