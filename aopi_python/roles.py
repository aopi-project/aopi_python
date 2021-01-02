from enum import Enum


class RolesEnum(str, Enum):
    read = "read"
    upload = "upload"
    proxy = "proxy"
