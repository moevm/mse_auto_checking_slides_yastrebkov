import db
from flask import request, jsonify


def _extract_token_from_request():
    if 'Authorization' not in request.headers:
        return None
    header_value = request.headers['Authorization']
    token = header_value.replace('Bearer ', '')
    return token


def _issue_token_to_user(related_actions):
    try:
        login = request.json['login']
        user_info = db.get_user_info(login)

        related_actions(user_info, login)

        return jsonify({
            'success': True,
            'token': db.generate_new_token_for_user(login)
        })
    except:
        return jsonify({
            'success': False,
        })


def sign_in():
    def related_actions(user_info, login):
        if user_info['password'] != request.json['password']:
            raise RuntimeError

    return _issue_token_to_user(related_actions)


def sign_up():
    def related_actions(user_info, login):
        print(user_info, login, request.json['password'])
        if user_info:
            raise RuntimeError
        db.create_user(login, request.json['password'])

    return _issue_token_to_user(related_actions)


def get_login():
    token = _extract_token_from_request()
    login = db.find_login_for_token(token)
    return login
