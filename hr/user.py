class UserHR:
    def __init__(self, db, app):
        self.db = db
        self._app = app

    def create_user(self, user):
        self.db.create_user_in_hr(user)
        return user