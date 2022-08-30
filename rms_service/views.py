import collections
from http import HTTPStatus
import json
import utils
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def config(request: HttpRequest) -> HttpResponse:
    error: BaseException
    try:
        if request.method == "POST":
            body: dict = json.loads(request.body)
            client = utils.get_restaurant_db_client()
            db = utils.get_restaurants_database(client)
            collection = utils.get_restaurants_collection(db)

            cursor = collection.find(
                {
                    "UniqueId": body["restaurantId"],
                    "Branches.UniqueId": body["branchId"],
                },
                projection={"_id": 0, "Branches.Users": 0},
            )
            data: list = []
            for c in cursor:
                document: dict = {
                    "UniqueId": c["UniqueId"],
                    "Name": c["Name"],
                    "Branches": [],
                }
                for b in c["Branches"]:
                    if b["UniqueId"] == body["branchId"]:
                        document["Branches"].append(b)
                        # for s in body['systems']:
                            

                data.append(document)

            cursor.close()
            client.close()
            return HttpResponse(
                json.dumps(data), content_type="application/json", status=HTTPStatus.OK
            )

    except Exception as e:
        print(e)
