from flask import *
from loginform import LoginForm
from signupform import SignUpForm
from db_connect import *

db = DB()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found 404'}), 404)


@app.route('/')
@app.route('/main')
def index():
    #news =  NewsModel(db.get_connection()).get_all(session['user_id'])
    #name = session['username'] if 'username' not in session else 'Пользователь'
    return render_template('main_list.html', title='Главная страница', username='Пользователь')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(db.get_connection())
        user_model.init_table()
        exists = user_model.exists(user_name, password)
        if (not exists[0]):
            user_model.insert(user_name, password)
        return redirect("/main")
    return render_template('signup.html', title='Регистрация', form=form)    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(db.get_connection())
        user_model.init_table()
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/main")
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect('/login')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')