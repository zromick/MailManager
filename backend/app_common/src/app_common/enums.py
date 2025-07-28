from enum import Enum


class MailItemStatus(Enum):
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"

    def __str__(self):
        return self.value
