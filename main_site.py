from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.users import RegisterForm
from flask_login import LoginManager, login_user
from forms.login import LoginForm
from data.jobs import Jobs
import datetime as dt

# добавляем логгер
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

loggined = False


# основная страница
@app.route('/')
def main_site():
    return render_template('main_menu.html')


# страница с одеждой (то же, что и основная)
@app.route('/clothes')
def clothes():
    return render_template('main_menu.html')


# страница с первой кофтой
@app.route('/clothes/gosha_adidas_black_longsleeve')
def clothes_gosha_black():
    return render_template('card_1.html')


# страница со второй кофтой
@app.route('/clothes/gosha_adidas_red_longsleeve')
def clothes_gosha_red():
    return render_template('card_2.html')


# страница с третьей кофтой
@app.route('/clothes/gosha_longsleeve_renessans')
def clothes_gosha_longsleeve_renessans():
    return render_template('card_3.html')


# нижний раздел privacy
@app.route('/privacy')
def privacy():
    f = open('static/text.txt')
    return render_template(f)


# загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# создаем базу
@app.route("/")
def index():
    db_sess = db_session.create_session()
    # jobs = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news="")


# регистрация
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    global loggined
    if not loggined:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        loggined = True
        return render_template('login.html', title='Авторизация', form=form)
    else:
        return render_template('main_menu.html')


# записываем первые данные в базу
def main():
    db_session.global_init("db/blogs1.db")
    user = User()
    user.surname = "Vanya"
    user.name = "Selyunin"
    user.age = 18
    user.position = "papa"
    user.speciality = 'head master'
    user.address = 'yandex_lyceum_1'
    user.email = 'selyushkaselyunin@gmail.com'
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    user = db_sess.query(User).filter(User.id == 1).first()
    jobs = Jobs(team_leader=1, job='deployment of residential modules 1 and 2', work_size=15, collaborators='2, 3',
                start_date=dt.datetime.now(), is_finished=False)
    db_sess.add(jobs)
    user.jobs.append(jobs)
    db_sess.commit()

    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Вторая новость", content="Уже вторая запись!",
    #             user=user, is_private=False)
    # db_sess.add(news)
    # db_sess.commit()
    #
    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Личная запись", content="Эта запись личная",
    #             is_private=True)
    # user.news.append(news)
    # db_sess.commit()

    app.run()


if __name__ == '__main__':
    main()
