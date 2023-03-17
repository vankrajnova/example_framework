from model import User, EmploymentStatus, UserInList, UserInfo
from rest.transaction import RestTransaction
from useful_methods.data_conversion import convert_to_full_xml_format, convert_utc_to_local


class UserRest:

    def __init__(self, app):
        self._app = app

    @staticmethod
    def _make_json_for_new_user(user: User) -> dict:
        json = {
            "lastName": user.info.last_name,
            "lastName_en": user.info.last_name_eng,
            "firstName": user.info.first_name,
            "firstName_en": user.info.first_name_eng,
            "additionalName": user.info.additional_name,
            "additionalName_en": user.info.additional_name_eng,
            "dateOfBirth": convert_to_full_xml_format(user.info.birthdate),
            "type": user.employment.user_type,
            "position": [user.employment.position.oid],
            "contractNumber": user.employment.contract_number,
            "dateFrom": convert_to_full_xml_format(user.employment.start_date),
            "workend": user.employment.lwd,
            "hrStatus": EmploymentStatus.get_status_by_value(user.employment.status).name.lower(),
            "manager": None if user.employment.manager_info is None else user.employment.manager_info.oid,
            "region": user.employment.region,
            "city": user.employment.city,
            "office": user.employment.office
        }
        return json

    @staticmethod
    def _make_user_in_list_from_json(user_as_json: dict, transaction: RestTransaction) -> UserInList:
        transaction.add_event('Распарсить json и вернуть из него UserInList')

        full_name = f'{user_as_json["familyName"]} {user_as_json["givenName"]} {user_as_json["additionalName"]}'
        position_name = user_as_json["employments"][0]["title"]
        dep_name = user_as_json["employments"][0]["org"]
        status = EmploymentStatus.get_status_by_name(user_as_json["employments"][0]["hrStatus"]).value
        email = None if user_as_json["email"] == "" else user_as_json["email"]
        return UserInList(
            full_name=full_name, position_name=position_name,
            department_name=dep_name, status=status, email=email)

    @staticmethod
    def _make_user_info_from_json(user_card_as_json: list[dict]) -> UserInfo:
        user_info = UserInfo()
        for item in user_card_as_json:
            match item["name"]:
                case "lastName":
                    user_info.last_name = item["value"]
                case "lastName_en":
                    user_info.last_name_eng = item["value"]
                case "firstName":
                    user_info.first_name = item["value"]
                case "firstName_en":
                    user_info.first_name_eng = item["value"]
                case "additionalName":
                    user_info.additional_name = item["value"]
                case "additionalName_en":
                    user_info.additional_name_eng = item["value"]
                case "dateOfBirth":
                    date_as_json = item["value"]
                    user_info.birthdate = convert_utc_to_local(date_as_json)
                case "name":
                    user_info.account_name = item["value"]
                case "telephoneNumber":
                    user_info.phone_number = item["value"]
                case "emailAddress":
                    user_info.email = item["value"]
        return user_info

    def create_user(
            self, user: User, logged_in_user: User = None,
    ) -> User:
        transaction = self._app.start_new_rest_transaction("Создать пользователя")

        path = f"/inrights/api/user/card/new?id=INRIGHTS.model.users.NewUser-2"
        json = self._make_json_for_new_user(user)

        transaction.call_request("PUT", path, logged_in_user=logged_in_user, json=json)
        return user

    def verify_user_in_user_list(self, user: User):
        transaction = self._app.start_new_rest_transaction(
            f'Проверить атрибуты пользователя "{user.info.account_name}" в списке пользователей'
        )
        user_as_json = self._get_user_from_user_list(user=user, transaction=transaction)
        actual_user_in_list = self._make_user_in_list_from_json(user_as_json[0], transaction)
        assert actual_user_in_list == user.in_list

    def verify_user_base_info(self, user: User):
        transaction = self._app.start_new_rest_transaction(
            f'Проверить атрибуты на вкладке "Информация о сотруднике" в карточке "{user.info.account_name}"'
        )
        actual_user_base_info = self._get_user_base_info(user, transaction)

        assert actual_user_base_info == user.info

    def _get_user_base_info(self, user: User, transaction: RestTransaction) -> UserInfo:
        transaction.add_event(f"Получить основную информацию о сотруднике {user.info.account_name}")
        user_card_as_json = self._get_user_card_as_json(user, transaction)
        user_info = self._make_user_info_from_json(user_card_as_json)
        return user_info

    def _get_user_card_as_json(self, user: User, transaction: RestTransaction) -> list[dict]:
        transaction.add_event(f"Получить json карточки пользователя {user.info.account_name}")
        path = f"/inrights/api/user/card/{user.info.oid}?sort="

        transaction.call_request("GET", path)
        items = transaction.check_items()
        return items

    def _get_user_from_user_list(
            self, user: User, logged_in_user: User = None, transaction: RestTransaction = None
    ) -> list[dict]:
        transaction.add_event(f'Получить item пользователя из списка пользователей')
        path = f"/inrights/api/users/list"

        json = {
            "operationId": None,
            "start": 0,
            "limit": 50,
            "sort": [
                {
                    "property": "familyName",
                    "direction": "ASC"
                }
            ],
            "filter":
                [
                    {
                        "property": "search",
                        "value": [f"{user.info.full_name}"],
                        "operator": "custom"}
                ]
        }

        transaction.call_request("POST", path, logged_in_user=logged_in_user, json=json)
        items = transaction.check_items()
        return items
