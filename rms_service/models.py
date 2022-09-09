import json
from django.http import HttpRequest


class AuthRequest:
    def __init__(self, request: HttpRequest) -> None:
        __body__: dict = json.loads(request.body)
        self.restaurantId: str = __body__["restaurantId"]
        self.branchId: str = __body__["branchId"]
        self.systems: list[BranchSystem] = []
        for i in __body__["systems"]:
            self.systems.append(BranchSystem(i["name"], i["uniqueId"]))


class BranchSystem:
    def __init__(self, name: str, unique_id: str) -> None:
        self.unique_id: str = unique_id
        self.name: str = name


class BranchDbMdl:
    def __init__(self, value: dict = {}) -> None:
        if "Name" in value:
            self.name: str = value["Name"]
            self.unique_id: str = value["UniqueId"]
            self.enabled: bool = value["Enabled"]
        else:
            self.name: str = ""
            self.unique_id: str = ""
            self.enabled: bool = False
        if "Users" in value:
            self.users: list[UserDbMdl] = list(
                map(self.__user_mapper__, value["Users"])
            )
        else:
            self.users = [UserDbMdl().get_dict()]
        if "Systems" in value:
            self.systems: list[SystemDbMdl] = list(
                map(self.__system_mapper__, value["Systems"])
            )
        else:
            self.systems = [SystemDbMdl().get_dict()]

    def get_dict(self) -> dict:
        print(2)
        return {
            "Name": self.name,
            "UniqueId": self.unique_id,
            "Enabled": self.enabled,
            "Systems": list(map(lambda x: x.get_dict(), self.systems)),
        }

    def __user_mapper__(self, value: dict):
        return UserDbMdl(value)

    def __system_mapper__(self, value: dict):
        return SystemDbMdl(value)


class RestaurantDbMdl:
    def __init__(self, value: dict = {}) -> None:
        if "Name" in value:
            self.name: str = value["Name"]
            self.unique_id: str = value["UniqueId"]
            self.enabled: bool = value["Enabled"]
        else:
            self.name = ""
            self.unique_id = ""
            self.enabled = False

        if "Branches" in value:
            self.branches: list[BranchDbMdl] = list(
                map(self.__mapper__, value["Branches"])
            )
        else:
            self.branches = []

    def __mapper__(self, value: dict = {}) -> BranchDbMdl:
        return BranchDbMdl(value)

    def get_dict(self) -> dict:
        print(1)
        return {
            "Name": self.name,
            "UniqueId": self.unique_id,
            "Enabled": self.enabled,
            "Branches": list(map(lambda x: x.get_dict(), self.branches)),
        }


class UserDbMdl:
    def __init__(self, value: dict = {}) -> None:
        if "Name" in value:
            self.name: str = value["Name"]
            self.unique_id: str = value["UniqueId"]
            self.enabled: bool = value["Enabled"]
        else:
            self.name = ""
            self.unique_id = ""
            self.enabled = False

    def get_dict(self) -> dict:
        print(3)
        return {"Name": self.name, "UniqueId": self.unique_id, "Enabled": self.enabled}


class SystemDbMdl:
    def __init__(self, value: dict = {}) -> None:
        if "Name" in value:
            self.name: str = value["Name"]
            self.unique_id: str = value["UniqueId"]
            self.enabled: bool = value["Enabled"]
        else:
            self.name = ""
            self.unique_id = ""
            self.enabled = False

    def get_dict(self) -> dict:
        print(4)
        return {"Name": self.name, "UniqueId": self.unique_id, "Enabled": self.enabled}
