from email import message
from hashlib import sha256
from urllib.parse import urlencode
from flask import (Flask,
                   request,
                   redirect,
                   render_template_string,
                   session,
                   render_template,
                   make_response
                   )
from requests import post
from re import match
from database import *

client_id = '6d75febd721740c8b6cf1c2045238e5a'
client_secret = '65ec566bd4544f0d923075752851484f'
oauthurl = 'https://oauth.yandex.ru/'
baseurl = "http://localhost:8000"

app = Flask(__name__)
app.secret_key = "QSKMALKMKM828324ASDOIWDJ898*&SD*A&H"

def negative(fullname):
    return True if not match("[a-zA-Z0-9а-яА-Я]", fullname) else False

def activate():
    import OPi.GPIO as GPIO
    from time import sleep

    GPIO.setboard(GPIO.PCPCPLUS)    
    GPIO.setmode(GPIO.BOARD)        
    GPIO.setup(7, GPIO.OUT)         
    GPIO.output(7, 1)
    sleep(40)
    GPIO.output(7, 0)
    GPIO.cleanup()

@app.route('/')
def main():
    if 'fullname' not in session:
        return make_response(redirect('/login'))
    else:
        return make_response(redirect('/index'))

@app.route('/exit')
def exit():
    session.clear()
    return make_response(redirect('/'))

@app.route('/index')
def index():
    if 'fullname' in session:
        string = f"Привет, {session['fullname']}!<br>Этот сервис позволяет согревать чаек, но функционал доступен только администраторам.<br>Так что можешь закрывать страницу, тебе не добраться до моего чая! :)"
        return render_template_string(string)
    else:
        return make_response(redirect('/login'))

@app.route('/oauth/yandex/info')
def oauthInfo():
    if request.args.get('token', False):
        access_token = request.args.get('token')
        result = post("https://login.yandex.ru/info", headers={"Authorization": f"bearer {access_token}"}).json()
        session['fullname'] = result['real_name']
        session['admin'] = False
        session['uid'] = "none"
        return redirect('/')
    else:
        return render_template_string("Ошибка!")

@app.route('/oauth/yandex/callback/')
def oauthLogin():
    if request.args.get('code', False):
        data = {
            'grant_type': 'authorization_code',
            'code': request.args.get('code'),
            'client_id': client_id,
            'client_secret': client_secret
        }
        data = urlencode(data)
        token = post(oauthurl + "token", data).json()
        try:
            access_token = token['access_token']
        except:
            return render_template_string("Ошибка!")
        return redirect(f"/oauth/yandex/info?token={access_token}")
    return render_template_string("Ошибка!")

@app.route('/oauth')
def yalogin():
    return redirect(oauthurl + f"authorize?response_type=code&client_id={client_id}")

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'fullname' in session:
        return make_response(redirect('/index'))
    if request.method == "POST":
        login = request.form.get("login")
        password = sha256(request.form.get("password").encode()).hexdigest()
        fullname = request.form.get('fullname')
        if negative(fullname):
            return render_template("register.html", message="Полное имя не может содержать ничего кроме букв и цифр!")
        try:
            Users.get(Users.login == login)
            return render_template("register.html", message="Пользователь с таким именем уже зарегестрирован")
        except:
            Users.create(login=login, password=password, fullname=fullname)
            return (make_response(redirect('/login')))
    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'fullname' in session:
        return make_response(redirect('/index'))
    if request.method == "POST":
        login = request.form.get("login")
        password = sha256(request.form.get("password").encode()).hexdigest()
        user = Users.get_or_none(Users.login == login, Users.password == password)
        if user is None:
            return render_template("login.html", message="Неверный логин или пароль")
        session['uid'] = user.user_id
        session['fullname'] = user.fullname
        session['admin'] = user.isAdmin
        return make_response(redirect('/index'))
    return render_template("login.html")

@app.route('/admin')
def admin():
    if not 'fullname' in session:
        return make_response(redirect('/login'))
    print(session)
    if not session['admin'] == True:
        return render_template_string("Ты точно не админ!")
    if request.method == "POST":
        activate()
        return render_template_string("Чаек уже греется")
    return render_template("admin.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)