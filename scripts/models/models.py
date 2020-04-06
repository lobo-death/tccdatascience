from peewee import *
from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    'bot',
    user='root',
    password='root',
    host='localhost')


class User(Model):
    id = AutoField()
    name = CharField(max_length=125)
    street = CharField(max_length=255)

    class Meta:
        database = db
        db_table = 'user'


class Product(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=75)
    price = DoubleField()

    class Meta:
        database = db
        db_table = 'product'


class Purchase(Model):
    id = AutoField()
    user_id = ForeignKeyField(User)

    class Meta:
        database = db
        db_table = 'purchase'


class Items(Model):
    id = AutoField()
    purchase_id = ForeignKeyField(Purchase)
    product_id = ForeignKeyField(Product)
    qt = DoubleField()

    class Meta:
        database = db
        db_table = 'items'


if __name__ == "__main__":
    try:
        User.create_table()
    except OperationalError:
        print
        "User table already exists!"

    try:
        Product.create_table()
    except OperationalError:
        print
        "Product table already exists!"

    try:
        Purchase.create_table()
    except OperationalError:
        print
        "Purchase table already exists!"

    try:
        Items.create_table()
    except OperationalError:
        print
        "Items table already exists!"
