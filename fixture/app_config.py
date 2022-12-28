from pydantic import BaseModel


class AppConfig(BaseModel):
    ip: str
    port: str
    admin_login: str
    admin_pwd: str
    browser: str
    interactive_mode: bool

    @property
    def host(self):
        return fr'http://{self.ip}:{self.port}'


def make_app_config_from_json(config_as_json):
    app_config = AppConfig(
        ip=config_as_json["ip"],
        port=config_as_json["port"],
        admin_login=config_as_json["admin_login"],
        admin_pwd=config_as_json["admin_pwd"],
        interactive_mode=config_as_json["interactive_mode"],
        browser=config_as_json["browser"]
    )
    return app_config
