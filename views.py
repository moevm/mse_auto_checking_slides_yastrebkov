from flask import render_template, request, redirect, Response, abort
from werkzeug.utils import secure_filename
from app import app
import os

user = {'username':'test_user'}


@app.route('/results/<id>')
def results(id):
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
    return render_template("checking.html", title="Checking results", results=results)


@app.route('/list')
@app.route('/list/<page>')
def list(page):
    main_list = [
        {
            'name': 'File 1',
            'id': 1
        },
        {
            'name': 'File 2',
            'id': 2
        },
        {
            'name': 'File 3',
            'id': 3
        },
        {
            'name': 'File 4',
            'id': 4
        },
        {
            'name': 'File 5',
            'id': 5
        },
        {
            'name': 'File 6',
            'id': 6
        },
        {
            'name': 'File 7',
            'id': 7
        },
        {
            'name': 'File 8',
            'id': 8
        },
        {
            'name': 'File 9',
            'id': 9
        },
        {
            'name': 'File 10',
            'id': 10
        },
        {
            'name': 'File 11',
            'id': 11
        },
        {
            'name': 'File 12',
            'id': 12
        },
        {
            'name': 'File 13',
            'id': 13
        },
        {
            'name': 'File 14',
            'id': 14
        },
        {
            'name': 'File 15',
            'id': 15
        },
        {
            'name': 'File 16',
            'id': 16
        },
        {
            'name': 'File 17',
            'id': 17
        },
        {
            'name': 'File 18',
            'id': 18
        },
        {
            'name': 'File 19',
            'id': 19
        },
        {
            'name': 'File 20',
            'id': 20
        },
        {
            'name': 'File 21',
            'id': 21
        },
        {
            'name': 'File 22',
            'id': 22
        },
        {
            'name': 'File 23',
            'id': 23
        },
        {
            'name': 'File 24',
            'id': 24
        },
        {
            'name': 'File 25',
            'id': 25
        },
        {
            'name': 'File 26',
            'id': 26
        },
        {
            'name': 'File 27',
            'id': 27
        },
        {
            'name': 'File 28',
            'id': 28
        },
        {
            'name': 'File 29',
            'id': 29
        },
        {
            'name': 'File 30',
            'id': 30
        },
        {
            'name': 'File 31',
            'id': 31
        },
        {
            'name': 'File 32',
            'id': 32
        }
    ]

    list = []

    if int(page)*10 < len(main_list):
        for number in range(10):
            list.append(main_list[(int(page)-1)*10+number])
        next_page=True
    else:
        for number in range(len(main_list) - ((int(page)-1)*10)):
            list.append(main_list[(int(page)-1)*10+number])
        next_page = False

    if int(page) == 1:
        prev_page = False
    else:
        prev_page = True

    return render_template("list.html", title="Data base", list=list, page_number = int(page), next_page=next_page, prev_page=prev_page)


@app.route('/home')
def home():
    return render_template("home.html", title="Home", user=user)


@app.route('/')
def main_page():
    return render_template("main_page.html")


@app.route('/sign-in', methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        print(request.form)
        return redirect("/home")
    else:
        return render_template("sign-in.html")


@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        print(request.form)
        return redirect("/home")
    else:
        return render_template("sign-up.html")


@app.route("/presentation", methods=["POST"])
def presentation():
    file = request.files["file"]
    data = file.stream.read()
    print(os.path.splitext(file.filename)[-1])
    if os.path.splitext(file.filename)[-1] not in [".ppt", ".pptx", ".odp", ".odpx"]:
        return render_template("upload_status.html", title="Upload status", success=False, user=user), 404
    with open(secure_filename(file.filename), "wb") as output_file:
        output_file.write(data)
    return render_template("upload_status.html", title="Upload status", success=True, user=user)


@app.route('/upload_presentation')
def upload_presentation():
    return render_template("upload_presentation.html", title="Upload presentation", user=user)

