from src.config.models import DinxBaseModel


class Users(DinxBaseModel, table=True):
    email: str
    password: str
    first_name: str
    last_name: str
    active: bool = True
    role: str
