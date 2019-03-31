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


@app.route('/')
@app.route('/main')
def main():    
    UserModel(db.get_connection()).init_table()
    ProductModel(db.get_connection()).init_table()
    if 'username' in session:
        name = session['username']
        products =  ProductModel(db.get_connection()).get_all()
        status = UserModel(db.get_connection()).get(session['user_id'])[3]
        id_us = session['user_id']
        BasketModel(db.get_connection()).init_table()
    else:
        name = 'Пользователь'
        products =  ProductModel(db.get_connection()).get_all()
        id_us = 'no_user'
        status = 'no' 
    return render_template('main_list.html', title='Главная страница', \
        username='Пользователь', \
        products= products,
        status= status,
        id= id_us)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if (not exists[0]):
            user_model.insert(user_name, password, 'user', 0, 0)
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
    return render_template('basket.html', title= 'Корзина', products= sp)

@app.route('/add_in_basket/<int:product_id>', methods=['GET', 'POST'])
def add_in(product_id):
    basket = BasketModel(db.get_connection())
    seller = ProductModel(db.get_connection()).get(product_id)[4]
    basket.insert(product_id, session['user_id'], seller)
    return redirect('/main')

@app.route('/buy_one_product/<int:product_id>/<int:page>', methods=['GET', 'UPDATE'])
def buy_one(product_id, page):
    basket = BasketModel(db.get_connection())
    basket.delete_one(product_id, session['user_id'])
    UserModel(db.get_connection()).new_buy(session['user_id'])
    seller = ProductModel(db.get_connection()).get(product_id)[4]
    UserModel(db.get_connection()).new_sale(seller)
    return redirect('/basket') if page == 2 else redirect('/main')

@app.route('/buy_all', methods=['GET'])
def buy_all():
    basket = BasketModel(db.get_connection())
    sp = basket.get_all(session['user_id'])
    prod = ProductModel(db.get_connection())
    UserModel(db.get_connection()).new_buy(session['user_id'], len(sp))
    for item in sp:
        UserModel(db.get_connection()).new_sale(item[1])
    basket.delete_for_buyer(session['user_id'])
    return redirect('/basket')

#-------------------------------------------

@app.route('/my_page', methods=['GET'])
def profile():
    user = UserModel(db.get_connection()).get(session['user_id'])
    my_products = ProductModel(db.get_connection()).get_all(session['user_id'])
    return render_template('my_page.html', user=user, products=my_products)

@app.route('/delite_my_profile', methods=['GET', 'DELETE'])
def delite_my_profile():
    BasketModel(db.get_connection()).delete_with_seller(session['user_id'])
    ProductModel(db.get_connection()).delete_with_user(session['user_id'])
    UserModel(db.get_connection()).delete_user(session['user_id'])
    return redirect('/logout')

#---------------------------------------------------

@app.route('/control_users', methods=['GET'])
def control_users():
    users = UserModel(db.get_connection()).get_all()
    print(users)
    return render_template('control_users.html', users= users)

@app.route('/delite_profile/<int:user_id>', methods=['GET', 'DELETE'])
def delite_profile(user_id):
    BasketModel(db.get_connection()).delete_with_seller(user_id)
    ProductModel(db.get_connection()).delete_with_user(user_id)
    UserModel(db.get_connection()).delete_user(user_id)
    return redirect('/control_users')

@app.route('/do_admin/<int:user_id>', methods=['GET', 'UPDATE'])
def do_admin(user_id):
    UserModel(db.get_connection()).do_admin(user_id)
    return redirect('/control_users')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')