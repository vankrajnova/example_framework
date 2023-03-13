from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from enum import Enum
import model.user_info


class EmploymentStatus(Enum):
    ACTIVE = "Работает"
    FIRED = "Уволен"
    VACATION = "В отпуске"
    MATERNITY = "В декретном отпуске"

    @staticmethod
    def get_status_by_value(value):
        for member in EmploymentStatus:
            if member.value == value:
                return member

    @staticmethod
    def get_status_by_name(name):
        for member in EmploymentStatus:
            if member.name == name:
                return member


class Employment(BaseModel):
    position: Optional[model.unit.Position]
    main: Optional[bool]
    start_date: Optional[str] = datetime.today().strftime("%d.%m.%Y")
    status: Optional[str] = EmploymentStatus.ACTIVE.value
    user_type: Optional[str] = "Selenium_auto"
    manager_info: Optional[model.user_info.UserInfo]
    contract_number: Optional[str]
    lwd: Optional[str]
    region: Optional[str] = "Region"
    city: Optional[str] = "City"
    office: Optional[str] = "Office"
    oid: Optional[str]
    emp_hr_id: Optional[str] = Field(exclude=True)

    class Config:
        arbitrary_types_allowed = True

    @property
    def full_name(self):
        return ", ".join(self.position.get_parent_chain_as_lines()) + ", " + self.position.name
