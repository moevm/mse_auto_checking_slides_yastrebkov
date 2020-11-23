from flask import Flask, send_from_directory, request, jsonify
import pymongo
from bson.objectid import ObjectId
from checking import Checker
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

with open("mongo-db-link-url.txt", "r") as f:
    db_url = f.readline()
client = pymongo.MongoClient(db_url)
db = client.Cluster0

db.users.create_index([('login', 1)], unique=True) # Will create the index only if it didn't already exist

def get_user_info(login):
    return db.users.find_one({'login': login})

def create_user(login, password):
    print(db.users.insert_one({
        'login': login,
        'password': password,
    }))

db.authTokens.create_index([('token', 1)], unique=True) # Will create the index only if it didn't already exist

def generate_token():
    from random import sample
    from string import ascii_letters, digits
    return "".join(sample(ascii_letters + digits, 32))


def generate_new_token_for_user(login):
    token = generate_token()
    db.authTokens.insert_one({
        'token': token,
        'login': login,
    })
    return token

def find_login_for_token(token):
    return db.authTokens.find_one({'token': token})['login']

def save_report(report):
    return str(db.reports.insert_one(report).inserted_id)

def join_report(report):
    report['id'] = str(report['_id'])
    del report['_id']
    for check in report['checks']:
        check['name'] = Checker.check_names[check['id']]

def get_joined_report(id):
    report = db.reports.find_one({'_id': ObjectId(id)})
    join_report(report)
    return report

def get_joined_reports_for_user(login):
    reports = list(reversed(list(db.reports.find({'userLogin': login}))))
    for report in reports:
        join_report(report)
    return reports

def extract_token_from_request(request):
    if 'Authorization' not in request.headers:
        return None
    header_value = request.headers['Authorization']
    token = header_value.replace('Bearer ', '')
    return token

@app.route('/api/sign-in', methods=["POST"])
def sing_in():
    req = request.json
    print(req)
    user_info = get_user_info(req['login'])
    if user_info and user_info['password'] == req['password']:
        return jsonify({
            'success': True,
            'token': generate_new_token_for_user(req['login'])
        })
    else:
        return jsonify({
            'success': False,
            'message': "Неверный логин или пароль",
        })

@app.route('/api/sign-up', methods=["POST"])
def sing_up():
    req = request.json
    print(req)
    user_info = get_user_info(req['login'])
    if not user_info:
        create_user(req['login'], req['password'])
        return jsonify({
            'success': True,
            'token': generate_new_token_for_user(req['login'])
        })
    else:
        return jsonify({
            'success': False,
            'message': "Пользователь с таким логином существует",
        })

@app.route('/api/check-presentation', methods=["POST"])
def check_presentation():
    req = request.json
    try:
        import io
        import base64
        presentation_file = io.BytesIO(base64.b64decode(req['presentation']))
        check_results = Checker.check(presentation_file)
        from datetime import datetime
        report = {
            'checks': check_results,
            'datetime': datetime.utcnow(),
            'fileName': req['fileName'],
        }
        if 'authToken' in req:
            login = find_login_for_token(req['authToken'])
            if login:
                report['userLogin'] = login
        report_id = save_report(report)
        return jsonify({
            'success': True,
            'reportId': report_id
        })
    except:
        return jsonify({
            'success': False,
        })

@app.route('/api/report/<id>', methods=["GET"])
def get_report(id):
    report = get_joined_report(id)
    if report:
        return jsonify({
            'success': True,
            'report': report
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Такая проверка не найдена :(',
        })

@app.route('/api/reports', methods=["GET"])
def get_reports():
    token = extract_token_from_request(request)
    if not token:
        print(request.headers)
        return jsonify({
            'success': True,
            'reports': []
        })

    login = find_login_for_token(token)
    if not login:
        return jsonify({
            'success': False,
        })

    reports = get_joined_reports_for_user(login)
    return jsonify({
        'success': True,
        'reports': reports
    })

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def public(path):
    path = 'index.html'
    return send_from_directory('public', path)

import os
app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

from checking import Checker