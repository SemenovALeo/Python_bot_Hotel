from datetime import datetime

from peewee import *


db = SqliteDatabase('database/User.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    class Meta:
        db_table = 'Users'

    user_id = IntegerField()
    username = CharField(max_length=120)
    command = CharField(max_length= 30)
    city = CharField(max_length=120)
    quantity_hotel = IntegerField()
    check_in = DateField()
    check_out =DateField()
    adults = IntegerField()
    created_date = DateTimeField(default=datetime.now)


class Order(BaseModel):
    class Meta:
        db_table = 'Orders'

    user = ForeignKeyField(User)
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    distance = IntegerField
    price = IntegerField
    website = CharField(max_length=255)