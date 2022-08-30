import collections
from http import HTTPStatus
import json
import utils
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def config(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        body: dict = json.load(request.body)
        client = utils.get_restaurant_db_client()
        db = utils.get_restaurants_database(client)
        collection = utils.get_restaurants_collection(db)

        cursor = collection.find(
            {"UniqueId": body["restaurantId"], "Branches.UniqueId": body["branchId"]},
            projection={"_id": 0, "Branches.Users": 0},
        )
        data: list = []
        for c in cursor:
            data.append(c)

        cursor.close()
        client.close()
        return HttpResponse(
            json.dumps(data), content_type="application/json", status=HTTPStatus.OK
        )
    else:
        return HttpResponse("", status=HTTPStatus.BAD_REQUEST)
