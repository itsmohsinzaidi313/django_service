from typing import NoReturn
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from http import HTTPStatus
import json
from rms_service.models import BranchSystem, RestaurantDbMdl, SystemDbMdl, AuthRequest
import utils
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def config(request: HttpRequest) -> HttpResponse:
    try:
        if request.method == "POST":
            auth_request: AuthRequest = AuthRequest(request)
            client = utils.get_restaurant_db_client()
            db = utils.get_restaurants_database(client)
            collection: Collection = utils.get_restaurants_collection(db)

            cursor: Cursor = collection.find(
                {
                    "UniqueId": auth_request.restaurantId,
                    "Branches.UniqueId": auth_request.branchId,
                },
                projection={"_id": 0},
            )
            data: list = []
            for c in cursor:
                doc: RestaurantDbMdl = RestaurantDbMdl(c)

                for b in doc.branches:
                    if b.unique_id == auth_request.branchId:
                        new_systems: list = extract_new_systems(
                            b.systems, auth_request.systems
                        )
                        if len(new_systems) > 0:
                            b.systems.append(new_systems)
                            x = doc
                            y = x.get_dict()
                            # collection.replace_one(
                            #     {"UniqueId": auth_request.restaurantId}, doc.get_dict()
                            # )

            cursor.close()
            client.close()
            return HttpResponse(
                json.dumps(data), content_type="application/json", status=HTTPStatus.OK
            )

    except Exception as e:
        print(e)
        return HttpResponse(e, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def extract_new_systems(old: list[SystemDbMdl], new: list[BranchSystem]) -> list:
    systems: list[SystemDbMdl] = []
    for a in new:
        exists: bool = False
        for b in old:
            if a.unique_id == b.unique_id:
                exists = True
                break
        if not exists:
            systems.append(a)
    return systems


def clean_up(my_dict: dict, auth: AuthRequest) -> NoReturn:
    b_count: int = 0
    for b in my_dict["Branches"]:
        if b["UniqueId"] == auth.branchId:
            count: int = 0
            while count < len(b["Systems"]):
                if not b["Systems"][count]["Enabled"]:
                    b["Systems"].pop(count)
                    count = 0
                count += 1

        else:
            my_dict["Branches"].pop(b_count)
        b_count += 1
