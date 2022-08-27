import json


class AppUser:
    def __init__(self, name: str = None, username: str = None, password: str = None, enabled: bool = None, request_body: str = None) -> None:
        if request_body:
            dict_obj: dict = json.loads(request_body)
            self.name = dict_obj.get('Name', '')
            self.username = dict_obj.get('Username', '')
            self.password = dict_obj.get('Passphrase', '')
            self.enabled = True if dict_obj.get('Enabled', 0) == 1 else False
        else:
            self.name = name
            self.username = username
            self.password = password
            self.enabled = enabled


class Restaurant:
    pass


class Branch:
    pass


class Shift:
    pass


class Order:
    pass


class MenuItem:
    pass


class Item(MenuItem):
    pass


class Deal(MenuItem):
    pass


class DealItem:
    pass
