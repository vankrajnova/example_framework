from rest.repository import RepositoryRest
from rest.user import UserRest


class RestFactory:

    def __init__(self, app):
        self.repository = RepositoryRest(app)
        self.user = UserRest(app)
