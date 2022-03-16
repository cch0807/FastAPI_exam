from enum import Enum


class ApplicationStatus(Enum):
    APPLIED = 0
    PROCESSING = 1
    PENDING = 2
    APPROVED = 3
    REJECTED = 4
