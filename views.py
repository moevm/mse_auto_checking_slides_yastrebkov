from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    results = [
        {
            'name': 'Check 1',
            'res': 'Ok'
        },
        {
            'name': 'Check 2',
            'res': 'Ok'
        },
        {
            'name': 'Check 3',
            'res': 'Ok'
        },
        {
            'name': 'Check 4',
            'res': 'Ok'
        },
        {
            'name': 'Check 5',
            'res': 'Ok'
        },
        {
            'name': 'Check 6',
            'res': 'Ok'
        },
        {
            'name': 'Check 7',
            'res': 'Ok'
        }
    ]
    return render_template("checking.html",title="Checking results", results=results)