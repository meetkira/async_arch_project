from enum import Enum


class Role(str, Enum):
    worker = "worker"
    admin = "admin"
    accountant = "accountant"
    manager = "manager"
