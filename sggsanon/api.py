from flask import Blueprint, render_template, abort, request, jsonify, Response
from pymongo import MongoClient
import time
import random, string
from flask_mail import Mail, Message
import os
client = MongoClient(os.environ['DATABASE_URL'])
db = client["message"]

api = Blueprint('api', __name__, template_folder='templates')



api.config.update(
    DEBUG=False,
    MAIL_SERVER='smtp-relay.brevo.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_DEFAULT_SENDER=('admin', 'admin@nicewhite.eu.org'),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME='yoni980807@gmail.com',
    MAIL_PASSWORD='LEZw5HG4JRzQBW9r'
)

mail = Mail(api)



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
        page = request.args.get('page')
    else:
        page = 1


    datas = db.mb_message.find().limit(limit).skip((page-1)*limit)
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
    

@api.route('/api/v1/login/', methods=['POST'])
def login():
    if not request.json:
        return jsonify({"error": "request must be json"}), 400
    if not request.json.get('uname') or not request.json.get('password'):
        return jsonify({"error": "uname and password are required"}), 400
    uname = request.json.get('uname')
    password = request.json.get('password')
    data = db.users.find_one({'uname': uname, 'password': password})
    if data:
        sessions = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10)) + uname
        db.session.insert_one({'uname': uname, 'login_time': time.time(),'session':sessions})
        return jsonify({"success": "login success",'session':sessions}), 200
    else:
        return jsonify({"error": "login failed"}), 400
    
@api.route('/api/v1/register/', methods=['POST'])
def register():

    uname = request.json.get('uname')
    password = request.json.get('password')
    email = request.json.get('email')
    verify_code = request.json.get('email_verify_code')


    if not request.json:
        return jsonify({"error": "request must be json"}), 400
    
    if not request.json.get('uname') or not request.json.get('password'):
        return jsonify({"error": "uname and password are required"}), 400
    
    if not request.json.get('email_verify_code'):
        return jsonify({"error": "email_verify_code is required"}), 400

    if not request.json.get('email'):
        return jsonify({"error": "email is required"}), 400
    
    if request.json.get('password') != request.json.get('password_verify'):
        return jsonify({"error": "passwords do not match"}), 400
    
    if db.users.find_one({'uname': uname}):
        return jsonify({"error": "username already exists,perhaps try another?"}), 400
    
    if not db.reg_code.find_one({"email":request.json.get('email'),"reg_code":request.json.get('email_verify_code')}): 
        return jsonify({"error": "email verify code is incorrect"}), 400

    if time.time() - db.reg_code.find_one({"email":email,"reg_code":verify_code})["send_time"] > 300: # 5 minutes
            db.reg_code.delete_one({"email":email,"reg_code":verify_code})
            abort(Response("驗證碼已過期!"))


    db.users.insert_one({'uname': uname, 'password': password, 'email': email,'reg_time':time.time(),'last_login_time':0})
    return jsonify({"success": "register success"}), 200


@api.route('/api/v1/register/email_verify', methods=['POST'])
def email_verify():
    email = request.json.get('email')
    if not request.json:
        return jsonify({"error": "request must be json"}), 400
    
    if not request.json.get('email'):
        return jsonify({"error": "email is required"}), 400
    
    if db.users.find_one({"email":email}):
        return jsonify({"error": "email with user already exists"}), 400
    
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
    return jsonify({"success": "email verify code sent"}), 200