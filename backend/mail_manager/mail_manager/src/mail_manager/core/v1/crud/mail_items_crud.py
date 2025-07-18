from functools import lru_cache

from app_common.enums import MailItemStatus
from app_common.logger import logger
from app_common.schemas import MailItemCreate, MailItemUpdate
from fastapi_pagination.ext.sqlalchemy import paginate
from mail_manager.api.v1.exceptions import MailItemNotFoundException
from mail_manager.core.v1 import models
from sqlalchemy import select
from sqlalchemy.orm import Session


class MailItemsCRUD:
    def create_mail_item(
        self, mail_item_create: MailItemCreate, session: Session
    ) -> models.MailItem:
        mail_item = models.MailItem(
            mail_item_created_by=mail_item_create.mail_item_created_by,
        )

        session.add(mail_item)
        session.commit()
        session.refresh(
            mail_item
        )  # Refresh to get auto-generated fields like UUID, created_time

        logger.info("Created new mail item: {}", mail_item.mail_item_uuid)
        return mail_item

    def get_mail_item(self, mail_item_uuid: str, session: Session) -> models.MailItem:
        mail_item = session.get(models.MailItem, mail_item_uuid)
        if mail_item is None:
            raise MailItemNotFoundException(
                f"Mail item with UUID {mail_item_uuid} not found."
            )
        return mail_item

    def get_all_mail_items(
        self,
        session: Session,
        limit: int = 10,
        offset: int = 0,
        ignore_pending: bool = False,
        ignore_complete: bool = False,
    ):
        logger.info(
            "Retrieving mail items with:\n"
            "limit: {}\n"
            "offset: {}\n"
            "ignore complete pending: {}\n"
            "ignore complete statuses: {}",
            limit,
            offset,
            ignore_pending,
            ignore_complete,
        )

        ignore_pending_filter = (
            models.MailItem.mail_item_review_status != MailItemStatus.PENDING
        )

        ignore_complete_filter = (
            models.MailItem.mail_item_review_status != MailItemStatus.COMPLETE
        )

        select_statement = select(models.MailItem)

        if ignore_pending:
            select_statement = select_statement.filter(ignore_pending_filter)

        if ignore_complete:
            select_statement = select_statement.filter(ignore_complete_filter)

        select_statement = select_statement.order_by(
            models.MailItem.mail_item_created_time.desc()
        )

        mail_item_db_entries = paginate(session, select_statement)

        return mail_item_db_entries

    def update_mail_item(
        self, mail_item_uuid: str, mail_item_update: MailItemUpdate, session: Session
    ) -> models.MailItem:
        mail_item = self.get_mail_item(mail_item_uuid, session)

        # Convert the Pydantic update model to a dictionary, excluding unset fields
        update_data = mail_item_update.model_dump(exclude_unset=True, exclude_none=True)

        # Apply updates to the SQLAlchemy ORM model
        for key, value in update_data.items():
            setattr(mail_item, key, value)

        session.add(mail_item)
        session.commit()
        session.refresh(mail_item)  # Refresh to get updated state from DB

        logger.info("Updated mail item {}: {}", mail_item_uuid, update_data)
        return mail_item


# singleton
@lru_cache(maxsize=1)
def get_mail_items_crud() -> MailItemsCRUD:
    return MailItemsCRUD()
