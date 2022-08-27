import json
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from http import HTTPStatus
import pymongo
from pymongo import cursor as crsr

from .models import AppUser
from django_service import settings
import utils


def login(request: HttpRequest) -> HttpResponse:
    app_user = AppUser(request_body=request.body)
    _dict = get_user_restaurant(app_user=app_user)

    if _dict.get('Name', '') == '':
        return HttpResponse('', status=HTTPStatus.UNAUTHORIZED)

    return HttpResponse(json.dumps(_dict), HTTPStatus.OK)


def sync(request: HttpRequest) -> HttpResponse:
    app_user = AppUser(request_body=request.body)
    _dict = get_user_restaurant(app_user=app_user)
    if _dict['Name'] == '':
        return HttpResponse(content='', status=HTTPStatus.UNAUTHORIZED)

    data: dict = {'Branches': []}
    client = utils.MongoClient(settings.CONNECTION_STRING)
    database = client.get_database(_dict['Name'])
    for b in _dict['Branches']:
        branch: dict = {
            'Name': b,
            'Shifts': []}
        collection = database.get_collection(b)
        cursor = collection.find(projection={'_id': 0}).sort(
            'ShiftId', pymongo.DESCENDING).limit(2)

        for c in cursor:
            shift: dict = c
            branch['Shifts'].append(shift)
        cursor.close()
        data['Branches'].append(branch)
    client.close()
    return HttpResponse(json.dumps(data), content_type='application/json', status=HTTPStatus.OK)


def get_data(request: HttpRequest) -> HttpResponse:
    app_user = AppUser(request_body=request.body)
    _dict = get_user_restaurant(app_user=app_user)

    if _dict['Name'] == '':
        return HttpResponse(content='', status=HTTPStatus.UNAUTHORIZED)

    decoded_json: dict = json.loads(request.body)

    client = utils.MongoClient(settings.CONNECTION_STRING)
    db = client.get_database(_dict['Name'])

    data: dict = {'Branches': []}

    for b in _dict['Branches']:

        branch: dict = {'Name': b, 'Shifts': []}
        collection = db.get_collection(b)

        value: list = []
        for a in decoded_json['Branches']:
            if a['Name'] == b:
                value = a['Shifts']
                break

        if len(value) > 0:
            condition: str = '$nin' if bool(
                decoded_json['Exclusive']) else '$in'

            cursor = collection.find(
                {'ShiftId': {condition: value}}, projection={'_id': 0})
            for c in cursor:
                branch['Shifts'].append(c)
            cursor.close()
            data['Branches'].append(branch)

    client.close()
    return HttpResponse(content=json.dumps(data), status=HTTPStatus.OK)


def get_shifts_list(request: HttpRequest) -> HttpResponse:
    app_user = AppUser(request_body=request.body)
    _dict = get_user_restaurant(app_user=app_user)

    if _dict['Name'] == '':
        return HttpResponse(content='', status=HTTPStatus.UNAUTHORIZED)

    client = utils.MongoClient(settings.CONNECTION_STRING)
    db = client.get_database(_dict['Name'])

    data: dict = {'Branches': []}

    for b in _dict['Branches']:
        branch: dict = {'Name': b, 'Shifts': []}
        collection = db.get_collection(b)
        cursor = collection.find({}, projection={
                                 '_id': 0, 'ShiftId': 1, 'ShiftNumber': 1}).sort('ShiftId', pymongo.ASCENDING)
        for c in cursor:
            branch['Shifts'].append(c)
        cursor.close()
        data['Branches'].append(branch)
    client.close()
    return HttpResponse(content=json.dumps(data), status=HTTPStatus.OK)


def get_user_restaurant(app_user: AppUser) -> dict:
    client = utils.MongoClient(settings.CONNECTION_STRING)
    database = client.get_database('Restaurants_db')
    collection = database.get_collection('Restaurants')
    # print(utils.encrypt_to_md5(app_user.password))
    cursor = collection.find(
        {'Branches.Users.Username': app_user.username, 'Branches.Users.Passphrase': app_user.password})
    _dict: dict = {}
    for r in cursor:
        _dict['Name'] = r['Name']
        for s in r['Branches']:
            if _dict.get('Branches', '') == '':
                _dict['Branches'] = []
            _dict['Branches'].append(s['Name'])

    cursor.close()
    client.close()
    return _dict
