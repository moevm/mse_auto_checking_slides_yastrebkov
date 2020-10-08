from flask import render_template, request, redirect, Response, abort
from werkzeug.utils import secure_filename
from app import app
import os


class User:
    def __init__(self, username='test_user', status=False, firstname="test", lastname="user", email="test_user@email.com"):
        self.is_signed = status
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email


class Check_settings:
    def __init__(self, s1=True, s2=True, s3=True, s4=True, s5=True, s6=True, s7=True):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.s4 = s4
        self.s5 = s5
        self.s6 = s6
        self.s7 = s7


main_list = []

for i in range(32):
    main_list.append({
        'name': 'File' + str(i),
        'id': i
    })

user = User()
check_setting = Check_settings()


@app.route('/results/<id>')
def results(id):
    results = []
    if check_setting.s1:
        results.append({
            'name': 'Check 1',
            'res': 'Ok'
        })
    if check_setting.s2:
        results.append({
            'name': 'Check 2',
            'res': 'Ok'
        })
    if check_setting.s3:
        results.append({
            'name': 'Check 3',
            'res': 'Ok'
        })
    if check_setting.s4:
        results.append({
            'name': 'Check 4',
            'res': 'Ok'
        })
    if check_setting.s5:
        results.append({
            'name': 'Check 5',
            'res': 'Ok'
        })
    if check_setting.s6:
        results.append({
            'name': 'Check 6',
            'res': 'Ok'
        })
    if check_setting.s7:
        results.append({
            'name': 'Check 7',
            'res': 'Ok'
        })
    return render_template("checking.html", title="Checking results", results=results, id=id)


@app.route('/list')
@app.route('/list/<page>')
def list(page):
    list = []

    if int(page) * 10 < len(main_list):
        for number in range(10):
            list.append(main_list[(int(page) - 1) * 10 + number])
        next_page = True
    else:
        for number in range(len(main_list) - ((int(page) - 1) * 10)):
            list.append(main_list[(int(page) - 1) * 10 + number])
        next_page = False

    if int(page) == 1:
        prev_page = False
    else:
        prev_page = True

    return render_template("list.html", title="Data base", list=list, page_number=int(page), next_page=next_page,
                           prev_page=prev_page, user=user)


@app.route('/home')
def home():
    return render_template("home.html", title="Home", user=user)


@app.route('/')
def main_page():
    if user.is_signed:
        return render_template("main_page.html", user=user)
    else:
        return render_template("main_page.html")


@app.route('/sign-in', methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        print(request.form)
        user.is_signed = True
        user.username = "test_user"
        return redirect("/home")
    else:
        return render_template("sign-in.html")


@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        print(request.form)
        user.is_signed = True
        user.username = request.form['username']
        user.email = request.form['email']
        user.firstname = request.form['firstName']
        user.lastname = request.form['lastName']
        return redirect("/home")
    else:
        return render_template("sign-up.html")


@app.route("/presentation", methods=["POST"])
def presentation():
    file = request.files["file"]
    data = file.stream.read()
    print(os.path.splitext(file.filename)[-1])
    if os.path.splitext(file.filename)[-1] not in [".ppt", ".pptx", ".odp", ".odpx"]:
        return render_template("upload_presentation.html", title="Upload presentation", success=False, user=user), 400
    with open(secure_filename(file.filename), "wb") as output_file:
        output_file.write(data)
    return render_template("upload_status.html", title="Upload status", success=True, user=user)


@app.route('/upload_presentation')
def upload_presentation():
    return render_template("upload_presentation.html", title="Upload presentation", success=True, user=user)


@app.route('/check_settings')
def check_settings():
    return render_template("check_settings.html", title="Check settings", user=user)


@app.route('/profile_settings')
def profile_settings():
    return render_template("profile_settings.html", title="Profile settings", user=user)


@app.route('/log_out', methods=["GET", "POST"])
def log_out():
    user.is_signed = False
    return redirect("/")


@app.route('/check_set', methods=["GET", "POST"])
def check_set():
    check_setting.s1 = request.form.get('Check1')
    check_setting.s2 = request.form.get('Check2')
    check_setting.s3 = request.form.get('Check3')
    check_setting.s4 = request.form.get('Check4')
    check_setting.s5 = request.form.get('Check5')
    check_setting.s6 = request.form.get('Check6')
    check_setting.s7 = request.form.get('Check7')
    return redirect("/home")


@app.route('/profile_set', methods=["GET", "POST"])
def profile_set():
    user.username = request.form['username']
    user.email = request.form['email']
    user.firstname = request.form['firstName']
    user.lastname = request.form['lastName']
    return redirect("/home")


@app.route('/delete_one/<id>')
def delete_one(id):
    for i in main_list:
        if int(i.get('id')) == int(id):
            main_list.remove(i)
    return redirect("/list/1")
