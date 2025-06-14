import re
from typing import Any, Dict, Union
from pydantic.errors import PydanticValueError

class PhoneError(PydanticValueError):
    code = 'phone'
    msg_template = 'value is not a valid phone number'


class PhoneStr(str):
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type='string', format='phone')

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str]) -> str:
        return validate_phone(value)

def validate_phone(value: str) -> str:
    if not re.match(r"^(01[3-9]\d{8})$", value):
        raise PhoneError()
    return value