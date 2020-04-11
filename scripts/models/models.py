from peewee import *
from peewee import PostgresqlDatabase
from environs import Env

env = Env()
env.read_env()

postgres_database = env("POSTGRES_DATABASE")
postgres_user = env("POSTGRES_USER")
postgres_password = env("POSTGRES_PASSWORD")
postgres_host = env("POSTGRES_HOST")

db = PostgresqlDatabase(
    postgres_database,
    user=postgres_user,
    password=postgres_password,
    host=postgres_host)


class User(Model):
    id = IntegerField(primary_key=True)
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
    user = ForeignKeyField(User)

    class Meta:
        database = db
        db_table = 'purchase'


class Items(Model):
    id = AutoField()
    purchase = ForeignKeyField(Purchase)
    product = ForeignKeyField(Product)
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

        data_source = [
            {'id': 1, 'name': 'Maminha Angus', 'price': 45.99},
            {'id': 2, 'name': 'Picanha Argentina Angus', 'price': 79.99},
            {'id': 3, 'name': 'Chorizo Angus', 'price': 52.99},
            {'id': 4, 'name': 'Entrecôt Angus', 'price': 59.99},
            {'id': 5, 'name': 'Peito', 'price': 16.99},
            {'id': 6, 'name': 'Tulipinha', 'price': 22.99},
            {'id': 7, 'name': 'Coxa', 'price': 19.99},
            {'id': 8, 'name': 'Coração', 'price': 12.99},
            {'id': 9, 'name': 'Lombinho', 'price': 13.99},
            {'id': 10, 'name': 'Panceta', 'price': 10.99},
            {'id': 11, 'name': 'Linguiça Toscana', 'price': 9.99}

        ]

        for data_dict in data_source:
            Product.create(**data_dict)

        print("All tables created and initials data inserted!")

    except OperationalError:
        print("Product table already exists!")

    try:
        Purchase.create_table()
    except OperationalError:
        print("Purchase table already exists!")

    try:
        Items.create_table()
    except OperationalError:
        print("Items table already exists!")
