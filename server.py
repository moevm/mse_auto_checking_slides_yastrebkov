from flask import Flask, send_from_directory, request, jsonify
from checking import Checker
import db
import authorization
from datetime import datetime

app = Flask(__name__)


app.route('/api/sign-in', methods=["POST"])(authorization.sign_in)
app.route('/api/sign-up', methods=["POST"])(authorization.sign_up)


def fileFromBase64(data):
    import io
    import base64
    return io.BytesIO(base64.b64decode(data))


@app.route('/api/check-presentation', methods=["POST"])
def check_presentation():
    try:
        presentation_file = fileFromBase64(request.json['presentation'])
        check_results = Checker.check(presentation_file, request.json['studentDegree'])
        report = {
            'checks': check_results,
            'datetime': datetime.utcnow(),
            'fileName': request.json['fileName'],
            'studentDegree': request.json['studentDegree'],
        }

        login = authorization.get_login()
        if login:
            report['userLogin'] = login

        report_id = db.save_report(report)
        return jsonify({
            'success': True,
            'reportId': report_id
        })
    except:
        return jsonify({
            'success': False,
        })


@app.route('/api/report/<id>')
def get_report(id):
    report = db.get_joined_report(id)
    if report:
        return jsonify({
            'success': True,
            'report': report
        })
    else:
        return jsonify({
            'success': False,
        })


@app.route('/api/reports')
def get_reports():
    login = authorization.get_login()
    reports = []
    if login:
        reports = db.get_joined_reports_for_user(login)
    return jsonify({
        'success': True,
        'reports': reports
    })


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_index_html(path):
    return send_from_directory('static', 'index.html')


import os

app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
