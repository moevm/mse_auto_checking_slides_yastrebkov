import pymongo

with open('mongodb-link-config.json') as f:
    import json
    _config = json.load(f)
_client = pymongo.MongoClient(_config['url'])
_db = _client[_config['dbName']]

# Will create the index only if it didn't already exist
_db.users.create_index([('login', 1)], unique=True)
_db.authTokens.create_index([('token', 1)], unique=True)


# Users:

def get_user_info(login):
    return _db.users.find_one({'login': login})


def create_user(login, password):
    print(_db.users.insert_one({
        'login': login,
        'password': password,
    }))


# Tokens:

def _generate_token():
    from random import sample
    from string import ascii_letters, digits
    return "".join(sample(ascii_letters + digits, 32))


def generate_new_token_for_user(login):
    token = _generate_token()
    _db.authTokens.insert_one({
        'token': token,
        'login': login,
    })
    return token


def find_login_for_token(token):
    return _db.authTokens.find_one({'token': token})['login']


# Reports:

def save_report(report):
    return str(_db.reports.insert_one(report).inserted_id)


def _join_report(report):
    report['id'] = str(report['_id'])
    del report['_id']
    for check in report['checks']:
        from checking import Checker
        check['name'] = Checker.check_names[check['id']]


def get_joined_report(id):
    from bson.objectid import ObjectId, InvalidId
    try:
        report = _db.reports.find_one({'_id': ObjectId(id)})
        _join_report(report)
        return report
    except InvalidId:
        return None


def get_joined_reports_for_user(login):
    reports = list(reversed(list(_db.reports.find({'userLogin': login}))))
    for report in reports:
        _join_report(report)
    return reports
