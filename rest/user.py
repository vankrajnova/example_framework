from model import User, EmploymentStatus
from useful_methods.data_conversion import convert_to_full_xml_format


class UserRest:

    def __init__(self, app):
        self._app = app

    @staticmethod
    def _make_json_for_new_user(user):
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

    def create_user(
            self, user: User, logged_in_user: User = None,
    ):
        transaction = self._app.start_new_rest_transaction("[REST] Создать пользователя")

        path = f"/inrights/api/user/card/new?id=INRIGHTS.model.users.NewUser-2"
        json = self._make_json_for_new_user(user)

        transaction.call_request("PUT", path, logged_in_user=logged_in_user, json=json)
        return user