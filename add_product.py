from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
 
class AddProductForm(FlaskForm):
    title = StringField('Название товара', validators=[DataRequired()])
    content = TextAreaField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    submit = SubmitField('Добавить')
