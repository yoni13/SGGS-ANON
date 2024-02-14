from flask import Blueprint, render_template, abort, request, jsonify
from pymongo import MongoClient
client = MongoClient("mongodb://root:efjkajekrdfk@192.168.1.119/")
db = client["message"]

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/api/v1/')
def index():
    return 'This is the sggs-anon API v1'

@api.route('/api/v1/mb_board/')
def mb_board():
    if request.args.get('limit'):
        limit = request.args.get('limit')
    else:
        limit = 10
    if request.args.get('page'):
        page = request.args.get('page')
    else:
        page = 1
    datas = db.mb_message.find().limit(limit).skip((page-1)*limit)
    res = []
    for data in datas:
        info = {'uname': data['uname'], 'content': data['content'], 'pub_time': data['pub_time'], 'post_id': data['post_id']}
        res.append(info)
    return jsonify(res)