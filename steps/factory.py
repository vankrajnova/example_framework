from steps.ad import ADSteps
from steps.user import UserSteps


class StepsFactory:
    def __init__(self, app):
        self.user = UserSteps(app)
        self.ad = ADSteps(app)
