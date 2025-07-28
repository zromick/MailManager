import datetime
import uuid

from app_common.enums import MailItemStatus
from mail_manager.core.v1.database import Base
from sqlalchemy import Boolean, Column, DateTime, Enum, String, Text


class MailItem(Base):
    __tablename__ = "mail_item"

    mail_item_uuid = Column(Text(length=36), primary_key=True)
    mail_item_created_time = Column(DateTime, nullable=False)
    mail_item_created_by = Column(String, nullable=False)
    mail_item_review_status = Column(
        Enum(MailItemStatus), nullable=False, default=MailItemStatus.PENDING
    )
    mail_item_final_notification_sent = Column(Boolean, default=False)

    def __init__(
        self,
        mail_item_created_by,
    ):
        super().__init__()
        self.mail_item_uuid = uuid.uuid4().__str__()
        self.mail_item_created_time = datetime.datetime.now(datetime.timezone.utc)
        self.mail_item_created_by = mail_item_created_by
        self.mail_item_review_status = MailItemStatus.PENDING
        self.mail_item_final_notification_sent = False
