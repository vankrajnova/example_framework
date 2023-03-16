from typing import Optional
from pydantic import BaseModel, Field
from useful_methods.data_generation import make_unique_name


class UserInfo(BaseModel):
    last_name: Optional[str]
    first_name: Optional[str]
    additional_name: Optional[str]
    last_name_eng: Optional[str] = "Auto"
    first_name_eng: Optional[str] = "Ismail"
    additional_name_eng: Optional[str] = "Ibragimovich"
    birthdate: Optional[str] = "01.01.1990"
    email: Optional[str] = Field(exclude=True)
    account_name: Optional[str]
    phone_number: Optional[str]
    password: Optional[str] = Field(exclude=True)
    oid: Optional[str]
    hr_id: Optional[str] = Field(exclude=True)
    risk_level: Optional[int] = Field(exclude=True)

    def __init__(self, **data):
        super().__init__(**data)
        if self.last_name is None:
            self.last_name = make_unique_name()
        if self.account_name is None:
            self.account_name = f"i.{'i.' if self.additional_name is not None else ''}{self.last_name.lower()}"

    def __lt__(self, other):
        return self.last_name < other.last_name

    @property
    def full_name(self):
        names = [self.last_name, self.first_name]
        if self.additional_name is not None:
            names.append(self.additional_name)
        full_name = " ".join(names)
        return full_name

    @property
    def last_name_and_initials(self):
        last_name_and_initials = f"{self.last_name} {self.first_name[0]}."
        if self.additional_name.strip() != "":
            last_name_and_initials += f"{self.additional_name[0]}."
        return last_name_and_initials

    def add_email(self):
        self.email = f"{self.last_name.lower()}@inrights.local"
        return self.email