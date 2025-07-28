from datetime import datetime

from app_common.enums import MailItemStatus
from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, field_validator


class MailItemBase(BaseModel):
    pass


class MailItemCreate(MailItemBase):
    mail_item_created_by: str

    @field_validator("mail_item_created_by")
    @classmethod
    def validate_mail_item_created_by(cls, value):
        if value is not None:
            try:
                validate_email(value)
            except EmailNotValidError as e:
                raise ValueError(f"Invalid email format: {value}") from e
        return value


class MailItemUpdate(MailItemBase):
    # fields are optional for PATCH requests
    mail_item_review_status: MailItemStatus | None = None
    mail_item_final_notification_sent: bool | None = None


class MailItem(MailItemCreate, MailItemUpdate):
    mail_item_uuid: str
    mail_item_created_time: datetime


class MailItem(MailItemCreate, MailItemUpdate):
    mail_item_uuid: str
    mail_item_created_time: datetime
    mail_item_review_status: MailItemStatus
    mail_item_final_notification_sent: bool = False
