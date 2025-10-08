from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app import db


class LoginForm(FlaskForm):
    poketrainer_id = StringField(
        "PokéTrainer ID",
        validators=[DataRequired(), Length(min=3, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
    )
    submit = SubmitField("Log In")


class RegForm(FlaskForm):
    poketrainer_id = StringField(
        "PokéTrainer ID",
        validators=[DataRequired(), Length(min=3, max=20)],
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    submit = SubmitField("Register")

from mongoengine import Document, StringField, IntField

class Item(Document):
    poketrainer_id = IntField(required = True, unique = True)


class Item(db.Document):
    meta = {'collection' : 'items'}
    item_id = db.IntField(required = True, unique = True)
    item_name = db.StringField(required = True)
    item_description = db.StringField()
    item_price = db.IntField(required = True)
    item_quantity = db.IntField(required = True)

    @staticmethod
    def get_item_by_id(item_id):
        return Item.objects(item_id = item_id).first()
    
    @staticmethod
    def save_item(item_id, item_name, item_description, item_price, item_quantity):
        item = Item(
            item_id = item_id, 
            item_name = item_name, 
            item_description = item_description, 
            item_price = item_price, 
            item_quantity = item_quantity
            )
        item.save()
        return item
    
    @staticmethod
    def get_all_items():
        return Item.objects()
    
    @staticmethod
    def delete_all_items():
        Item.drop_collection()