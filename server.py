from flask import *
from loginform import LoginForm
from signupform import SignUpForm
from db_connect import DB
from User import UserModel
from basket import BasketModel
from products import ProductModel
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
        BasketModel(db.get_connection()).init_table()
    else:
        name = 'Пользователь'
        products =  ProductModel(db.get_connection()).get_all()
        status = 'no_user'
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

#--------------------------------------  

@app.route('/products',  methods=['GET'])
def get_products():
    products = ProductModel(db.get_connection()).get_all()
    return jsonify({'product': products})

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

@app.route('/delete_product/<int:product_id>', methods=['GET'])
def delete_product1(product_id):
    if 'username' not in session:
        return redirect('/login')
    nm = ProductModel(db.get_connection())
    nm.delete(product_id)
    bas = BasketModel(db.get_connection())
    bas.delete_with_product(product_id)
    return redirect("/")

#---------------------------------------------------

@app.route('/basket')
def basket1():
    basket = BasketModel(db.get_connection()).get_all(session['user_id'])
    prod = ProductModel(db.get_connection())
    if len(basket) > 0:
        sp = [prod.get(i[0]) for i in basket]
    else:
        sp = 'Пусто'
    print(sp)
    return render_template('basket.html', title= 'Корзина', products= sp)

@app.route('/add_in_basket/<int:product_id>', methods=['GET', 'POST'])
def add_in(product_id):
    basket = BasketModel(db.get_connection())
    basket.insert(product_id, session['user_id'])
    return redirect('/main')

@app.route('/buy_one_product/<int:product_id>', methods=['GET'])
def buy_one(product_id):
    basket = BasketModel(db.get_connection())
    basket.delete_one(product_id, session['user_id'])
    return redirect('/basket')

@app.route('/buy_all', methods=['GET'])
def buy_all():
    basket = BasketModel(db.get_connection())
    basket.delete_for_buyer(session['user_id'])
    return redirect('/basket')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')