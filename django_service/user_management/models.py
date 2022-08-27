import json


class AppUser:
    def __init__(self,  request_body: str = None) -> None:
        dict_obj: dict = json.loads(request_body)
        self.restaurant: str = dict_obj.get('Restaurant', '')
        self.branches: str = dict_obj.get('Branches', '')
        self.name: str = dict_obj.get('Name', '')
        self.username: str = dict_obj.get('Username', '')
        self.password: str = dict_obj.get('Password', '')
        self.enabled: bool = dict_obj.get('Enabled', True)

    def get_dict(self) -> dict:
        return {'Name': self.name,
                'Username': self.username,
                'Password': self.password,
                'Enabled': self.enabled, }
