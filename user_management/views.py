from http.client import HTTPResponse
import json
from user_management.models import AppUser
import utils
from pymongo import cursor as crsr
from http import HTTPStatus
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.core.handlers.wsgi import WSGIRequest

CONTENT_TYPE = "application/json"


def users(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        app_user = AppUser(request.body)
        if not username_exists(app_user.username):
            add_user(app_user)
        else:
            return HTTPResponse(
                "User already exists",
                content_type=CONTENT_TYPE,
                status=HTTPStatus.NOT_FOUND,
            )
        return JsonResponse("", content_type=CONTENT_TYPE)
    elif request.method == "PUT":
        app_user = AppUser(request.body)
        if username_exists(app_user.username):
            update_user(app_user)
        return JsonResponse("", content_type=CONTENT_TYPE)
    elif request.method == "DELETE":
        app_user = AppUser(request.body)
        if username_exists(app_user.username):
            delete_user(app_user)
        return JsonResponse("", content_type=CONTENT_TYPE)
    else:
        return JsonResponse(status=HTTPStatus.BAD_REQUEST)


def view_users(request: WSGIRequest) -> HTTPResponse:
    e: BaseException
    try:
        client = utils.get_restaurant_db_client()
        db = utils.get_restaurants_database(client)
        users_collection = utils.get_users_collection(db)
        cursor = users_collection.find(projection={"_id": 0})

        users_list: list = []
        for c in cursor:
            users_list.append(c)

        cursor.close()
        client.close()
        context = {}
        context["title"] = "User Management"
        context["users"] = users_list
        return render(request, "list_table.html", context)
    except (e):
        print(e)
        return HTTPResponse("error", status=HTTPStatus.INTERNAL_SERVER_ERROR)


def username_exists(username: str) -> bool:
    client = utils.get_restaurant_db_client()
    db = utils.get_restaurants_database(client)
    collection = utils.get_restaurants_collection(db)
    cursor = collection.find(
        {"Branches.Users.Username": username}, projection={"_id": 0}
    )
    documents: list = []
    for c in cursor:
        documents.append(c)
    cursor.close()
    client.close()
    return len(documents) > 0


def add_user(user: AppUser) -> bool:
    client = utils.get_restaurant_db_client()
    db = utils.get_restaurants_database(client)
    collection = utils.get_restaurants_collection(db)
    cursor = collection.find({"Name": user.restaurant})
    for c in cursor:
        temp_dict: dict = c
        for branch in temp_dict["Branches"]:
            temp_users: list = branch["Users"]
            temp_users.append(user.get_dict())
        collection.replace_one(
            filter={"UniqueId": temp_dict["UniqueId"]}, replacement=temp_dict
        )


def update_user(user: AppUser) -> bool:
    client = utils.get_restaurant_db_client()
    db = utils.get_restaurants_database(client)
    collection = utils.get_restaurants_collection(db)
    cursor = collection.find({"Name": user.restaurant})
    for c in cursor:
        temp_dict: dict = c
        for branch in temp_dict["Branches"]:
            for user in branch["Users"]:
                if user["Username"] == user.username:
                    user["Name"] = user.name
                    user["Password"] = user.password
                    user["Enabled"] = user.enabled
                    break

        collection.replace_one(
            filter={"UniqueId": temp_dict["UniqueId"]}, replacement=temp_dict
        )

    cursor.close()
    client.close()
    return True


def delete_user(user: AppUser) -> bool:
    client = utils.get_restaurant_db_client()
    db = utils.get_restaurants_database(client)
    collection = utils.get_restaurants_collection(db)
    cursor = collection.find({"Name": user.restaurant})
    for c in cursor:
        temp_dict: dict = c
        for branch in temp_dict["Branches"]:
            for user in list(branch["Users"]):
                if user["Username"] == user.username:
                    list.remove(user)
                    break

        collection.replace_one(
            filter={"UniqueId": temp_dict["UniqueId"]}, replacement=temp_dict
        )

    cursor.close()
    client.close()
    return True
