from model import User, Orgunit, Position

# Some static objects for tests. The objects saved in DB backup.

class BaseFixture:

    def __init__(self, db_type):
        self.db_type = db_type

        self.administrator = self.add_user(last_name='Administrator',
                                           first_name='inRights',
                                           oid='00000000-0000-0000-0000-000000000002',
                                           account_name='administrator',
                                           password='5ecr3t')

        self.orgunit_1 = self.add_org_unit(name='01_Отдел автоматизации',
                                           oid='21b866f4-ce31-4837-9e42-b31cf7749568',
                                           oid_mssql='cce6e91a-a38a-48c1-b929-105b5e14476f',
                                           hr_id='btir2430',
                                           hr_id_mssql='cnom1830')

        self.orgunit_1_1 = self.add_org_unit(name='Подразделение автоматизации тестирования',
                                             oid='a76e3313-fb5c-4ec4-a926-2c86fa12579e',
                                             oid_mssql='1706218d-14b4-452a-936a-6268ba2ac9f0',
                                             hr_id='jbof1488',
                                             hr_id_mssql='vvtq5309')

        self.position_01 = self.add_position(name='Автотестировщик',
                                             oid="2114fc15-4ed1-4c69-a867-871ac1644fee",
                                             oid_mssql='5acf04df-a964-4458-943e-25741432f45b',
                                             hr_id='luad6058',
                                             hr_id_mssql='rwsc1556')

        self.orgunit_1.add_child(self.orgunit_1_1)
        self.orgunit_1_1.add_child(self.position_01)

    def add_user(self, last_name=None, first_name=None, additional_name=None,
                 oid=None, oid_mssql=None,
                 account_name=None, password=None, password_in_mssql=None):
        if self.db_type == 'postgresql':
            current_oid = oid
            current_password = password
        else:
            if oid_mssql is not None:
                current_oid = oid_mssql
            else:
                current_oid = oid
            if password_in_mssql is None:
                current_password = password
            else:
                current_password = password_in_mssql
        user = User(last_name=last_name, first_name=first_name, additional_name=additional_name,
                    oid=current_oid, account_name=account_name, password=current_password)
        return user

    def add_org_unit(self, name, oid, oid_mssql, hr_id=None, hr_id_mssql=None):
        if self.db_type == 'postgresql':
            return Orgunit(name=name, oid=oid, hr_id=hr_id)
        else:
            return Orgunit(name=name, oid=oid_mssql, hr_id=hr_id_mssql)

    def add_position(self, name, oid, oid_mssql, hr_id=None, hr_id_mssql=None):
        if self.db_type == 'postgresql':
            return Position(name=name, oid=oid, hr_id=hr_id)
        else:
            return Position(name=name, oid=oid_mssql, hr_id=hr_id_mssql)