import jwt
from flask import Flask, render_template, request, redirect, make_response

SECRET_KEY = 'butterfly'
ERROR_MESSAGE = '''
К сожалению, этот функционал доступен только для администраторов.
Если вы администратор, напишите в поддержку: support@google.com
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def hello_world():
    return render_template('welcome.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html')
    if request.method == 'POST':
        session = jwt.encode({'email': request.form['email'], 'role': 'guest'}, SECRET_KEY, algorithm='HS256')
        response = make_response(redirect('/home'))
        response.set_cookie('session', session)
        return response


@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        if 'session' not in request.cookies:
            raise jwt.InvalidTokenError
        session = jwt.decode(request.cookies['session'], SECRET_KEY, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return redirect('/auth')
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        role = session['role']
        if role != 'admin':
            return render_template('home.html', error=ERROR_MESSAGE)
        # Success PINs goes here !!!
        return render_template('home.html')


if __name__ == '__main__':
    app.run()
