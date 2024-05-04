import json
import logging
from excel_diary import make_json
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, redirect, render_template, abort, request, jsonify
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from data import db_session
from data.users import User
from alice import handle_dialog

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = '9vTgySlnidzBGrf'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/main_page')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main_page")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        f = request.files['file']
        f = f.read()
        with open("diary_files/Diary.xlsx", 'wb') as file:
            file.write(f)
        make_json()
        return render_template('main_page.html', title='Главная страница', success='Файл был загружен в систему')
    return render_template('main_page.html', title='Главная страница')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        print('a')
        if form.hashed_password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
        )
        user.set_password(form.hashed_password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        "session": request.json['session'],
        "version": request.json['version'],
        "response": {
            "end_session": False,
        },
        'session_state': request.json.get('state', {}).get('session', {})
    }
    if not response['session_state']:
        response['session_state'] = {"user_class": 0}

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    response['response']['tts'] = response['response']['text']
    return jsonify(response)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
