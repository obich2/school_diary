from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, redirect, render_template, abort, request
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from data import db_session
from data.users import User

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
        with open("../diary_files/Diary.xlsx", 'wb') as file:
            file.write(f)
        return "Форма отправлена"
    return render_template('main_page.html', title='Главная страница')

# @app.route('/authorized', methods=['GET', 'POST'])
# def main():
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).all()
#     query = db_sess.query(User)
#     crew_members = []
#     for user in db_sess.query(User).all():
#         crew_members.append((user.surname, user.name))
#
#     return render_template('jobs.html', jobs=jobs, crew=crew_members)
#
#
# @app.route('/add_jobs', methods=['GET', 'POST'])
# @login_required
# def add_jobs():
#     form = JobsForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         jobs = Jobs()
#         jobs.job = form.job.data
#         jobs.team_leader = form.team_leader.data
#         jobs.work_size = form.work_size.data
#         jobs.collaborators = form.collaborators.data
#         jobs.is_finished = form.is_finished.data
#         current_user.jobs.append(jobs)
#         db_sess.merge(current_user)
#         db_sess.commit()
#         return redirect('/authorized')
#     return render_template('add_jobs.html', title='Постановка задачи',
#                            form=form)
#
#
# @app.route('/add_jobs/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_news(id):
#     form = JobsForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         jobs = db_sess.query(Jobs).filter(Jobs.id == id,
#                                           ).first()
#         if jobs:
#             form.job.data = jobs.job
#             form.team_leader.data = jobs.team_leader
#             form.work_size.data = jobs.work_size
#             form.collaborators.data = jobs.collaborators
#             form.is_finished.data = jobs.is_finished
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         jobs = db_sess.query(Jobs).filter(Jobs.id == id,
#                                           ).first()
#         if jobs:
#             jobs.job = form.job.data
#             jobs.team_leader = form.team_leader.data
#             jobs.work_size = form.work_size.data
#             jobs.collaborators = form.collaborators.data
#             jobs.is_finished = form.is_finished.data
#             db_sess.commit()
#             return redirect('/authorized')
#         else:
#             abort(404)
#     return render_template('add_jobs.html',
#                            title='Редактирование задания',
#                            form=form
#                            )
#
#
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


#
#
# @app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def news_delete(id):
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).filter(Jobs.id == id,
#                                       ).first()
#     if jobs:
#         db_sess.delete(jobs)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/authorized')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
