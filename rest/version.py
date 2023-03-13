def get_build_info(app):
    transaction = app.start_new_rest_transaction("[REST] Получить информацию о версии приложения")
    response = transaction.call_request("GET", "inrights/api/version")
    try:
        return response["about"]["build"]
    except KeyError:
        transaction.raise_exception(exception_message="Не удалось обработать json")
