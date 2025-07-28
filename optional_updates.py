```python
# Set (Unordered, mutable, no duplicates) - Menu items
# Tuple (Ordered, immutable, duplicates) - Coordinates

class MailItem(Base):
    mail_item_status = Column(
        Enum(MailItemStatus), nullable=False, default=MailItemStatus.PENDING
    )
    mail_item_final_notification_sent = Column(Boolean, default=False)
+    mail_item_message = Column(String, nullable=False)

    def __init__(
        self,
        mail_item_created_by,
+        mail_item_message,
    ):
        super().__init__()
        self.mail_item_uuid = uuid.uuid4().__str__()
        # @@ -27,3 +29,4 @@ class MailItem(Base):
        self.mail_item_created_by = mail_item_created_by
        self.mail_item_review_status = MailItemStatus.PENDING
        self.mail_item_final_notification_sent = False
+        self.mail_item_message = mail_item_message


class MailItemCreate(MailItemBase):
    mail_item_created_by: str
+    mail_item_message: str


class MailItemUpdate(MailItemBase):
    # fields are optional for PATCH requests
    mail_item_review_status: MailItemStatus | None = None
    mail_item_final_notification_sent: bool | None = None
+    mail_item_message: str | None = None


def get_all_mail_items(
    limit: int = 10,
    offset: int = 0,
    ignore_complete: bool = False,
+    search: str = "",
    db: Session = Depends(get_db),
):
    return mail_items_crud.get_all_mail_items(
+        db, limit, offset, ignore_complete, search
    )


class MailItemsCRUD:
    def create_mail_item(
        self, db: Session, mail_item_create: schemas.MailItemCreate
    ) -> models.MailItem:
        mail_item = models.MailItem(
            mail_item_created_by=mail_item_create.mail_item_created_by,
+            mail_item_message=mail_item_create.mail_item_message,
        )
        db.add(mail_item)
        db.commit()
        db.refresh(mail_item)
        return mail_item

    def get_all_mail_items(
        self,
        db: Session,
        limit: int = 10,
        offset: int = 0,
        ignore_complete: bool = False,
        search: str = "",
    ):
        logger.info(
            "Retrieving mail items with:\n"
            "limit: {}\n"
            "offset: {}\n"
            "ignore complete statuses: {}\n"
            "search string: {}",
            limit,
            offset,
            ignore_complete,
            search,
        )

        select_statement = select(models.MailItem)

        if ignore_complete:
            select_statement = select_statement.filter(
                models.MailItem.mail_item_review_status != MailItemStatus.COMPLETE
            )

+        if search:
+            select_statement = select_statement.filter(
+                models.MailItem.mail_item_message.ilike(f"%{search}%")
+            )

        return db.execute(select_statement).scalars().all()

{
    field: 'mail_item_message', description: '', headerText: 'Message', minWidth: 300, valueGetter: undefined, sortable: true,
}
```

SORTING FOR ONE ITEM


It seems like you've provided two distinct blocks of sorting logic, and then a final select_statement.order_by that would override any previous sorting.

I'll provide the combined and corrected version that incorporates the multi-column sorting logic you outlined, ensuring it's the only sorting applied.

import logging
from sqlalchemy.orm import Session
from sqlalchemy import select, asc, desc
from sqlalchemy_pagination import paginate
from typing import Literal, List # Import List for clarity, though list[str] is fine in 3.9+

from . import models
from .models import MailItemStatus

logger = logging.getLogger(__name__)

class MailItemService:
def get_all_mail_items(
    self,
    session: Session,
    limit: int = 10,
    offset: int = 0,
    ignore_complete: bool = False,
    search: str = "",
    sort_by: List[str] = [], # Changed to List[str]
    sort_order: Literal["asc", "desc"] = "desc",
):
    logger.info(
        "Retrieving mail items with:\n"
        "limit: {}\n"
        "offset: {}\n"
        "ignore complete statuses: {}\n"
        "search string: {}\n"
        "sort_by: {}\n"
        "sort_order: {}",
        limit,
        offset,
        ignore_complete,
        search,
        sort_by,
        sort_order,
    )

    ignore_complete_filter = (
        models.MailItem.mail_item_review_status != MailItemStatus.COMPLETE
    )

    select_statement = select(models.MailItem)

    if ignore_complete:
        select_statement = select_statement.filter(ignore_complete_filter)

    if search:
        select_statement = select_statement.filter(
            models.MailItem.mail_item_message.ilike(f"%{search}%")
        )

    sortable_columns = {
        "mail_item_uuid": models.MailItem.mail_item_uuid,
        "mail_item_created_by": models.MailItem.mail_item_created_by,
        "mail_item_created_time": models.MailItem.mail_item_created_time,
        "mail_item_message": models.MailItem.mail_item_message,
        "mail_item_review_status": models.MailItem.mail_item_review_status,
        "mail_item_final_notification_sent": models.MailItem.mail_item_final_notification_sent,
    }

    order_clauses = []

    # Iterate through the provided sort_by columns
    if sort_by: # Only process if sort_by list is not empty
        for col_name in sort_by:
            if col_name in sortable_columns:
                column_to_sort = sortable_columns[col_name]
                if sort_order == "asc":
                    order_clauses.append(asc(column_to_sort))
                else: # Must be "desc" due to Literal validation
                    order_clauses.append(desc(column_to_sort))
            else:
                logger.warning(f"Invalid sort_by column '{col_name}' provided. Ignoring.")
    
    # If no valid sort columns were provided (either sort_by was empty, or all were invalid),
    # apply a default sort.
    if not order_clauses:
        order_clauses.append(models.MailItem.mail_item_created_time.desc())

    # Apply all collected order clauses
    select_statement = select_statement.order_by(*order_clauses) # Unpack the list of order clauses

    mail_item_db_entries = paginate(session, select_statement)

    return mail_item_db_entries



MULTI SORT BY


    1. FastAPI Endpoint (router.py or similar)
This is the code for your API route.

# router.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Literal, List # Import List for list type hint

from app.database import get_db
from app.crud import mail_items_crud # Assuming your service is in app/crud/mail_items_crud.py
from app.schemas import GenericLimitOffsetPage, MailItem
from app.exceptions import handle_unauthorized

router = APIRouter()

@router.get("/v1/mail_items/", response_model=GenericLimitOffsetPage[MailItem])
@handle_unauthorized
def get_all_mail_items(
limit: int = 10,
offset: int = 0,
ignore_complete: bool = False,
search: str = "",
# sort_by is now a list of strings, using Query to handle multiple values
sort_by: List[str] = Query([], description="List of columns to sort by. Can be repeated (e.g., ?sort_by=col1&sort_by=col2)"),
# sort_order is a Literal, ensuring it's either 'asc' or 'desc'
sort_order: Literal["asc", "desc"] = "desc",
db: Session = Depends(get_db),
):
return mail_items_crud.get_all_mail_items(
    db,
    limit,
    offset,
    ignore_complete,
    search,
    sort_by,
    sort_order
)

2. MailItemService Method (mail_items_crud.py or similar)
This is the code for your service layer function that interacts with the database.

# mail_items_crud.py

import logging
from sqlalchemy.orm import Session
from sqlalchemy import select, asc, desc
from sqlalchemy_pagination import paginate
from typing import Literal, List # Import List for list type hint

from . import models # Assuming models.py contains your SQLAlchemy models
from .models import MailItemStatus # Assuming MailItemStatus is defined in models

logger = logging.getLogger(__name__)

class MailItemService:
def get_all_mail_items(
    self,
    session: Session,
    limit: int = 10,
    offset: int = 0,
    ignore_complete: bool = False,
    search: str = "",
    sort_by: List[str] = [], # Expects a list of strings for multi-column sort
    sort_order: Literal["asc", "desc"] = "desc", # Expects 'asc' or 'desc'
):
    logger.info(
        "Retrieving mail items with:\n"
        "limit: {}\n"
        "offset: {}\n"
        "ignore complete statuses: {}\n"
        "search string: {}\n"
        "sort_by: {}\n"
        "sort_order: {}",
        limit,
        offset,
        ignore_complete,
        search,
        sort_by,
        sort_order,
    )

    ignore_complete_filter = (
        models.MailItem.mail_item_review_status != MailItemStatus.COMPLETE
    )

    select_statement = select(models.MailItem)

    if ignore_complete:
        select_statement = select_statement.filter(ignore_complete_filter)

    if search:
        select_statement = select_statement.filter(
            models.MailItem.mail_item_message.ilike(f"%{search}%")
        )

    # Define the mapping from frontend sort_by names to SQLAlchemy model attributes
    sortable_columns = {
        "mail_item_uuid": models.MailItem.mail_item_uuid,
        "mail_item_created_by": models.MailItem.mail_item_created_by,
        "mail_item_created_time": models.MailItem.mail_item_created_time,
        "mail_item_message": models.MailItem.mail_item_message,
        "mail_item_review_status": models.MailItem.mail_item_review_status,
        "mail_item_final_notification_sent": models.MailItem.mail_item_final_notification_sent,
        # Add other sortable columns here as needed
    }

    order_clauses = []

    # Iterate through the provided sort_by columns from the frontend
    if sort_by: # Only proceed if the sort_by list is not empty
        for col_name in sort_by:
            # Check if the requested column name is in our allowed sortable_columns map
            if col_name in sortable_columns:
                column_to_sort = sortable_columns[col_name]
                
                # Apply the single sort_order (asc or desc) to the current column
                if sort_order == "asc":
                    order_clauses.append(asc(column_to_sort))
                else: # Guaranteed to be "desc" due to FastAPI's Literal validation
                    order_clauses.append(desc(column_to_sort))
            else:
                # Log a warning if an invalid column name was requested for sorting
                logger.warning(f"Invalid sort_by column '{col_name}' provided. Ignoring.")
    
    # If no valid sort columns were added to order_clauses (e.g., sort_by was empty,
    # or all provided columns were invalid), apply a default sort.
    if not order_clauses:
        order_clauses.append(models.MailItem.mail_item_created_time.desc())

    # Apply all collected order clauses to the select statement.
    # The '*' unpacks the list, passing each clause as a separate argument to order_by.
    select_statement = select_statement.order_by(*order_clauses)

    mail_item_db_entries = paginate(session, select_statement)

    return mail_item_db_entries