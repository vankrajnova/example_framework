import psycopg2


class Postgresql:

    def __init__(self, host, name, user, pwd, port, db_type='postgresql'):
        self.host = host
        self.name = name
        self.user = user
        self.pwd = pwd
        self.port = port
        self.db_type = db_type
        self.connection = psycopg2.connect(host=host, port=int(port), database=name,
                                           user=user, password=pwd)

    def destroy(self):
        self.connection.close()
