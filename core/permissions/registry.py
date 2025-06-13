from enum import Enum
from .perms import IsAdmin
class Permission(Enum):
    admin = IsAdmin