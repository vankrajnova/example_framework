import pymssql


class MSSQL:

    def __init__(self, host, name, user, pwd, port, db_type='mssql'):
        self.host = host
        self.name = name
        self.user = user
        self.pwd = pwd
        self.port = port
        self.db_type = db_type
        self.connection = pymssql.connect(host=host, port=int(port), user=user, password=pwd, database=name)

    def destroy(self):
        self.connection.close()

    # todo: сюда по аналогии с class Postgresql необходимо добавить методы для создания пользователя в БД