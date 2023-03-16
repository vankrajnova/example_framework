import itertools

import psycopg2

from model import User
from useful_methods.data_conversion import format_date_for_hr
from useful_methods.data_generation import generate_id_for_hr, generate_phone_number


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

    def create_user_in_hr(self, user) -> User:
        user = self._prepare_user_info_for_hr(user)

        self._create_user_in_hr(user)
        self._create_employment_in_hr(user)

        return user

    def _prepare_user_info_for_hr(self, user) -> User:
        while True:
            user_id = generate_id_for_hr()
            if user_id not in self._get_employee_numbers():
                break
        while True:
            emp_id = generate_id_for_hr()
            if emp_id not in self._get_unique_ids():
                break

        user.info.hr_id = user_id
        user.employment.emp_hr_id = emp_id
        user.info.last_name_eng = None
        user.info.first_name_eng = None
        user.info.additional_name_eng = None
        user.info.phone_number = generate_phone_number()
        user.info.add_email()
        user.in_list.email = user.info.email
        user.employment.user_type = "штатный"
        user.employment.city = None

        return user

    def _create_user_with_employment_in_hr(self, user):
        """Создаёт пользователя и ТУ"""
        self._create_user_in_hr(user)
        self._create_employment_in_hr(user)

    def _create_user_in_hr(self, user):
        """Создает запись о пользователе без ТУ в таблице staff"""
        cursor = self.connection.cursor()
        try:
            sql = "INSERT INTO staff VALUES" \
                  "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            cursor.execute(sql % (user.info.hr_id, user.info.last_name, user.info.first_name,
                                  user.info.additional_name, format_date_for_hr(user.info.birthdate),
                                  user.info.phone_number, user.info.account_name, user.info.email))
            self.connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Ошибка при выполнении SQL запроса", error)
        finally:
            cursor.close()

    def _create_employment_in_hr(self, user, main=True):
        cursor = self.connection.cursor()

        try:
            emp = user.employment if main else user.additional_employment
            dep_name = emp.position.get_parent().name
            dep_id = emp.position.get_parent().hr_id
            pos_name = emp.position.name
            pos_id = emp.position.hr_id
            emp_main = 1 if emp.main else 0

            sql = "INSERT INTO " \
                  "employment" \
                  "(unique_id, last_name, first_name, middle_name, birth_date, employee_number, " \
                  "department_unique_id, position_unique_id, employee_status, employment_status," \
                  "work_start, office, region, department_name, position_name)" \
                  "VALUES" \
                  "('%s', '%s', '%s', '%s', '%s', '%s', " \
                  "'%s', '%s', %d, %d, '%s', " \
                  "'%s', '%s', '%s', '%s')"
            cursor.execute(sql % (emp.emp_hr_id, user.info.last_name, user.info.first_name,
                                  user.info.additional_name, user.info.birthdate, user.info.hr_id,
                                  dep_id, pos_id, 1, emp_main, format_date_for_hr(emp.start_date),
                                  emp.office, emp.region, dep_name, pos_name))
            self.connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Ошибка при выполнении SQL запроса", error)
        finally:
            cursor.close()

    def _get_employee_numbers(self) -> list:
        """Возвращает список employee_number всех пользователей из таблицы staff"""
        cursor = self.connection.cursor()
        converter = []

        try:
            sql = "SELECT employee_number FROM staff"
            cursor.execute(sql)

            self.connection.commit()

            for row in cursor:
                record = row
                converter.append(record)

        except (Exception, psycopg2.Error) as error:
            print("Ошибка при выполнении SQL запроса", error)

        finally:
            cursor.close()
        user_ids_list = list(itertools.chain(*converter))
        return user_ids_list

    def _get_unique_ids(self) -> list:
        """Возвращает список unique_id всех ТУ из таблицы employment"""
        cursor = self.connection.cursor()
        converter = []

        try:
            sql = "SELECT unique_id FROM employment"
            cursor.execute(sql)

            self.connection.commit()

            for row in cursor:
                record = row
                converter.append(record)

        except (Exception, psycopg2.Error) as error:
            print("Ошибка при выполнении SQL запроса", error)

        finally:
            cursor.close()
        emp_ids_list = list(itertools.chain(*converter))
        return emp_ids_list
