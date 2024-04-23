from flask import Blueprint, render_template, abort, request, jsonify
from pymongo import MongoClient
import os
client = MongoClient(os.environ['DATABASE_URL'])
db = client["message"]

api = Blueprint('api', __name__, template_folder='templates')

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
    
