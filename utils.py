import hashlib
from http import client
from pymongo import MongoClient, database
from pymongo import cursor as crsr
from django_service import settings


def get_db_handle(db_name: str, host, port, username, password):

    client = MongoClient(host=host,
                         port=int(port),
                         username=username,
                         password=password
                         )
    db_handle = client[db_name]
    return db_handle, client


def get_restaurant_db_client() -> MongoClient:
    return MongoClient(settings.CONNECTION_STRING)


def get_restaurants_database(client: MongoClient) -> database.Database:
    return client.get_database('Restaurants_db')


def get_restaurants_collection(database: database.Database):
    return database.get_collection('Restaurants')


def get_users_collection(database: database.Database):
    return database.get_collection('Users')


def encrypt_to_md5(value: str) -> str:
    result = hashlib.md5(value.encode())
    return result.hexdigest()
