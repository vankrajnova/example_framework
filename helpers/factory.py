from helpers.pwsh import PowerShellHelper


class HelpersFactory:
    def __init__(self, app):
        self.pwsh = PowerShellHelper(app.config)
