def get_build_info(app):
    transaction = app.start_new_rest_transaction('Получить информацию о версии приложения')
    transaction.set_request_url(fr'{app.config.host}/inrights/api/version')
    response = transaction.call_request("GET")
    build = response.json()["about"]["build"]
    return build
