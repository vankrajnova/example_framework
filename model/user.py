from typing import Optional
from pydantic import BaseModel
import model.employment
import model.user_info


class User:
    def __init__(self, last_name=None, first_name="Исмаил", additional_name="Ибрагимович", position=None,
                 main=True, manager_info=None, account_name=None, email=None, oid=None, password="Qwe12345"):
        self.info = model.user_info.UserInfo(
            last_name=last_name, first_name=first_name, additional_name=additional_name,
            account_name=account_name, email=email, oid=oid, password=password,
        )
        self.in_list = UserInList(full_name=self.info.full_name, email=self.info.email)
        if position is not None:
            self.employment = model.employment.Employment(
                position=position, main=main, manager_info=manager_info
            )
            self.in_list.position_name = self.employment.position.name
            self.in_list.department_name = self.employment.position.get_parent().name
            self.in_list.status = self.employment.status
            self.roles = position.calculate_all_base_roles()
        self.additional_employment = None

    def __eq__(self, other):
        if self.additional_employment is not None:
            return (
                    self.info == other.info
                    and self.employment == other.employment
                    and self.additional_employment == other.additional_employment
            )
        elif self.employment is not None:
            return self.info == other.info and self.employment == other.employment
        else:
            return self.info == other.info

    def __repr__(self):
        if self.employment is not None:
            return repr(self.info) and repr(self.employment)
        else:
            return repr(self.info)

    def __str__(self):
        if self.employment is not None:
            return (
                f"UserInfo: {str(self.info)},\n" f"Employment: {str(self.employment)}"
            )
        else:
            return f"UserInfo: {str(self.info)}"

    def __hash__(self):
        return hash(self.info.full_name)


class UserInList(BaseModel):
    full_name: Optional[str]
    position_name: Optional[str]
    department_name: Optional[str]
    status: Optional[str]
    email: Optional[str]
