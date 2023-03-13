from forms.auth import FormLogin
from forms.main import FormMain
from forms.user.form_user_list import FormUserList
from forms.user.form_user_new import FormUserNew


class FormFactory:
    def __init__(self, app):
        self.auth = FormLogin(app)
        self.user_list = FormUserList(app)
        self.user_new = FormUserNew(app)
        self.main = FormMain(app)

    def open_form_user_list(self) -> FormUserList:
        self.user_list.open()
        return self.user_list
