import os
from app import app
from flask_login import LoginManager
from flask import send_from_directory
from flask import render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from pymongo import *
from checks import checking
import shutil


app.config["MONGO_URI"] = "mongodb://localhost:27017/"
app.secret_key = 'super secret key'

login = LoginManager(app)

client = MongoClient('localhost', 27017)

db = client['PresVSDB']

Users = db['Users']
Files = db['Files']
Settings = db['Settings']
Results = db['Results']


login.login_view = 'login'


class User:

    def __init__(self, _id, username, email, firstname, lastname, password, searching=None):
        self.searching = searching
        self.role = "user"
        self._id = _id
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.email

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


    @login.user_loader
    def load_user(email):
        user = Users.find_one({'email': email})
        if user:
            user_obj = User(user['_id'], user['username'], user['email'], user['firstname'], user['lastname'],  user['password'], user.get('searching'))
            return user_obj
        else:
            return None


    @app.route('/sign-in', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect("/home")
        if request.method == "POST":
            user = Users.find_one({"email": request.form['email']})
            if user and user['password'] == request.form['password']:
                user_obj = User(user['_id'], user['username'], user['email'], user['firstname'], user['lastname'],  user['password'])
                login_user(user_obj, remember=bool(request.form.get('remember_me')))
                return redirect(url_for('home', title='Home', user=current_user))
            else:
                return render_template('sign-in.html', title='Sign In', success=False)
        else:
            return render_template('sign-in.html', title='Sign In', success=True)


    @app.route('/sign-up', methods=['GET', 'POST'])
    def registrate():
        if current_user.is_authenticated:
            return redirect("/home")
        if request.method == "POST":
            user = Users.find_one({"email": request.form['email']})
            if user:
                return render_template('sign-up.html', title='Sign up', success=False)
            else:
                Users.save({
                    'username': request.form.get('username'),
                    'email': request.form.get('email'),
                    'firstname': request.form.get('firstname'),
                    'lastname': request.form.get('lastname'),
                    'password': request.form.get('password')
                })
                user = Users.find_one({"email": request.form['email']})
                Settings.save(
                    {
                        'owner': user['_id'],
                        's1': True,
                        's2': True,
                        's3': True,
                        's4': True,
                        's5': True,
                        's6': True,
                        's7': True
                    }
                )
                user = Users.find_one({'email': request.form.get('email')})
                user_obj = User(user['_id'], user['username'], user['email'], user['firstname'], user['lastname'],  user['password'])
                login_user(user_obj)
                return redirect(url_for('home', title='Home', user=current_user))
        else:
            return render_template('sign-up.html', title='Sign up', success=True)


@login_required
@app.route('/log_out')
def log_out():
    logout_user()
    return redirect("/")


@login_required
@app.route('/results/<id>')
def results(id):
    results = []
    check_setting = Settings.find_one({'owner': current_user._id})
    res = Results.find_one({'file': id})
    if check_setting['s1']:
        results.append({
            'name': 'Check 1',
            'res': res['res1']
        })
    if check_setting['s2']:
        results.append({
            'name': 'Check 2',
            'res': res['res2']
        })
    if check_setting['s3']:
        results.append({
            'name': 'Check 3',
            'res': res['res3']
        })
    if check_setting['s4']:
        results.append({
            'name': 'Check 4',
            'res': res['res4']
        })
    if check_setting['s5']:
        results.append({
            'name': 'Check 5',
            'res': res['res5']
        })
    if check_setting['s6']:
        results.append({
            'name': 'Check 6',
            'res': res['res6']
        })
    if check_setting['s7']:
        results.append({
            'name': 'Check 7',
            'res': res['res7']
        })
    return render_template("checking.html", title="Checking results", results=results, id=id, user=current_user)


@login_required
@app.route('/list/<page>')
@app.route('/list/<page>', methods=["POST", "GET"])
def list(page=1):
    list = []

    cursor = Files.find({
        'owner': current_user._id
    })
    main_list = []
    fname = None
    if request.method == "POST":
        fname = request.form.get("File-name")
        if fname==None:
            fname = current_user.searching
        Users.update({'_id': current_user._id},
                     {
            'username': current_user.username,
            'email': current_user.email,
            'firstname': current_user.firstname,
            'lastname': current_user.lastname,
            'password': current_user.password,
            'searching': fname
        })
        if fname == None:
            for elem in cursor:
                main_list.append(elem)
        else:
            for elem in cursor:
                str_name = elem['name']
                if str_name.count(fname):
                    main_list.append(elem)
    else:
        Users.update({'_id': current_user._id},
                     {
                         'username': current_user.username,
                         'email': current_user.email,
                         'firstname': current_user.firstname,
                         'lastname': current_user.lastname,
                         'password': current_user.password,
                     })
        for elem in cursor:
            main_list.append(elem)

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
    if fname == None:
        return render_template("list.html", title="Data base", list=list, page_number=int(page), next_page=next_page,
                            prev_page=prev_page, user=current_user)
    else:
        return render_template("list.html", title="Data base", list=list, page_number=int(page), next_page=next_page,
                            prev_page=prev_page, user=current_user, val=fname)


@login_required
@app.route('/home')
def home():
    return render_template("home.html", title="Home", user=current_user)


@app.route('/')
def main_page():
    if current_user.is_authenticated:
        print(current_user.username)
        return redirect("/upload_presentation")
    else:
        return render_template("main_page.html")


@login_required
@app.route("/presentation", methods=["POST"])
def presentation():
    file = request.files["file"]
    if os.path.splitext(file.filename)[-1] not in [".ppt", ".pptx", ".odp", ".odpx"]:
        return render_template("upload_presentation.html", title="Upload presentation", success=False, user=current_user), 400
    res = checking(file)
    id =  Files.save({
        'owner': current_user._id,
        'name': file.filename,
    })
    f = open('config.txt', 'r')
    dir = f.readline()
    f.close()
    path =  os.path.join('files',str(current_user._id), str(id))

    Files.update({'_id': id},{
        'owner': current_user._id,
        'name': file.filename,
        'path': path
    })

    os.makedirs(os.path.join( dir, path), mode=0o777, exist_ok=False)
    file.save(os.path.join( dir, path, file.filename))

    Results.save({
        "file": str(id),
        "res1": res[0],
        "res2": res[1],
        "res3": res[2],
        "res4": res[3],
        "res5": res[4],
        "res6": res[5],
        "res7": res[6],
    })

    return redirect("/results/"+str(id))


@login_required
@app.route('/upload_presentation')
def upload_presentation():
    return render_template("upload_presentation.html", title="Upload presentation", success=True, user=current_user)


@login_required
@app.route('/check_settings')
def check_settings():
    return render_template("check_settings.html", title="Check settings", user=current_user)


@login_required
@app.route('/profile_settings')
def profile_settings():
    return render_template("profile_settings.html", title="Profile settings", user=current_user)


@login_required
@app.route('/check_set', methods=["GET", "POST"])
def check_set():
    s1 = bool(request.form.get('Check1'))
    s2 = bool(request.form.get('Check2'))
    s3 = bool(request.form.get('Check3'))
    s4 = bool(request.form.get('Check4'))
    s5 = bool(request.form.get('Check5'))
    s6 = bool(request.form.get('Check6'))
    s7 = bool(request.form.get('Check7'))
    Settings.update({'owner': current_user._id}, {
        'owner': current_user._id,
        's1': s1,
        's2': s2,
        's3': s3,
        's4': s4,
        's5': s5,
        's6': s6,
        's7': s7
    })
    return redirect("/home")


@login_required
@app.route('/profile_set', methods=["GET", "POST"])
def profile_set():
    Users.update({'_id': current_user._id}, {
        'email': request.form['email'],
        'username': request.form['username'],
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'password': current_user.password
    })
    logout_user()
    user = Users.find_one({'email': request.form['email']})
    user_obj = User(user['_id'], user['username'], user['email'], user['firstname'], user['lastname'],  user['password'])
    login_user(user_obj)
    return redirect("/home")

@login_required
@app.route('/download/<id>')
def download(id):
    f = open('config.txt', 'r')
    dir = f.readline()
    f.close()
    curs = Files.find({
        'owner': current_user._id
    })
    for elem in curs:
        if str(elem['_id']) == id:
            return send_from_directory(os.path.join(dir, elem['path']),filename=elem['name'], attachment_filename=elem['name'], as_attachment=True)
            break


@login_required
@app.route('/delete_one/<id>')
def delete_one(id):
    f =open('config.txt', 'r')
    dir = f.readline()
    f.close()
    Results.delete_one({
        'file': id
    })
    curs = Files.find({
        'owner': current_user._id
    })
    for elem in curs:
        if str(elem['_id']) == id:
            res = elem['_id']
            shutil.rmtree(os.path.join(dir, elem['path']))
            Files.delete_one({
                '_id': res
            })
            break

    return redirect("/list/1")
