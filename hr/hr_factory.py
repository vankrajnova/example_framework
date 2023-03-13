from hr.user import UserHR


class HrFactory:

    def __init__(self, app):
        self.user = UserHR(app.db, app)
