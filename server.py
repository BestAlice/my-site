from flask import *
from loginform import LoginForm
from signupform import SignUpForm
from db_connect import DB, UserModel, ProductModel
from add_product import AddProductForm

db = DB()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found 404'}), 404)

#session['user_id'] пригодится

@app.route('/')
@app.route('/main')
def main():    
    nm = ProductModel(db.get_connection())
    nm.init_table()
    if 'username' in session:
        name = session['username']
        products =  ProductModel(db.get_connection()).get_all()
        status = session['user_id']
    else:
        name = 'Пользователь'
        products =  ProductModel(db.get_connection()).get_all()
        status = 'no user'
    return render_template('main_list.html', title='Главная страница', \
        username='Пользователь', \
        products= products,
        status= status)

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
            user_model.insert(user_name, password, 'user')
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
        print(UserModel(db.get_connection()).get(exists[1]))
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/main")
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect('/main')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'username' not in session:
        return redirect('/login')
    form = AddProductForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        price = form.price.data
        nm = ProductModel(db.get_connection())
        nm.insert(title, content, price, session['user_id'])
        return redirect("/main")
    return render_template('add_product.html', title='Добавление Товара',
                           form=form, username=session['username'])

@app.route('/products',  methods=['GET'])
def get_products():
    products = ProductModel(db.get_connection()).get_all()
    return jsonify({'product': products})

@app.route('/product/<int:product_id>',  methods=['GET'])
def get_one_product(product_id):
    product = ProductModel(db.get_connection()).get(product_id)
    if not product:
        return jsonify({'error': 'Not found this product'})
    return jsonify({'product': product})

@app.route('/products', methods=['POST'])
def create_product():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'content', 'price', 'user_id']):
        return jsonify({'error': 'Bad request'})
    product = ProductModel(db.get_connection())
    product.insert(request.json['title'], request.json['content'],
                request.json['price'], request.json['user_id'])
    return jsonify({'success': 'OK'})

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = ProductModel(db.get_connection())
    if not product.get(product_id):
        return jsonify({'error': 'Not found'})
    product.delete(product_id)
    return jsonify({'success': 'OK'})

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')