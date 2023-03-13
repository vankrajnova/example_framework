import time
from rest.transaction import TIMEOUT, STEP_TIME


def _make_json_for_filtering_repository_objects(
        obj_type: str, obj_name: str, system_oid: str = None
) -> dict:
    filter_value = [
        {
            "value": [obj_type],
            "property": "type",
            "operator": "=",
        },
        {
            "value": [obj_name],
            "property": "search",
            "operator": "custom",
        },
    ]
    if system_oid:
        filter_value.append(
            {
                "value": [system_oid],
                "property": "systemOid",
                "operator": "=",
            }
        )
    json = {
        "start": 0,
        "limit": 25,
        "sort": [
            {
                "property": "name",
                "direction": "ASC",
            },
        ],
        "filter": filter_value,
    }
    return json


class RepositoryRest:

    def __init__(self, app):
        self._app = app

    def get_user_oid(self, user_last_name: str) -> str:
        return self._get_oid_by_obj_name("UserType", user_last_name)

    def _get_oid_by_obj_name(
            self, obj_type: str, obj_name: str, system_oid: str = None
    ) -> str:
        start = time.time()
        while (time.time() - start) < TIMEOUT:
            oid = self._try_to_get_oid_by_obj_name(obj_type, obj_name, system_oid)
            if oid is not None:
                return oid
            time.sleep(STEP_TIME)
        raise ValueError(f'Объект с именем "{obj_name}" не существует')

    def _try_to_get_oid_by_obj_name(
            self, obj_type: str, obj_name: str, system_oid: str = None
    ) -> str | None:
        transaction = self._app.start_new_rest_transaction(
            f'[REST] Получить oid объекта "{obj_name}" ({obj_type})'
        )
        path = "/inrights/api/technical/objects/list"
        json = _make_json_for_filtering_repository_objects(
            obj_type, obj_name, system_oid=system_oid
        )
        transaction.call_request("POST", path, json=json)
        items = transaction.check_items()

        if len(items) == 0:
            return None
        else:
            return items[0]['oid']
