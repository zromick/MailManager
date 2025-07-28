from app_common.pagination import GenericLimitOffsetPage
from app_common.schemas import MailItem, MailItemCreate, MailItemUpdate
from fastapi import APIRouter, Depends
from mail_manager.api.v1.exceptions import (
    handle_invalid_mail_item_reference,
    handle_mail_item_not_found,
    handle_unauthorized,
)
from mail_manager.core.v1.crud.mail_items_crud import get_mail_items_crud
from mail_manager.core.v1.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

mail_items_crud = get_mail_items_crud()


@router.get("/v1/mail_items/{mail_item_uuid}", response_model=MailItem)
@handle_unauthorized
@handle_mail_item_not_found
def get_mail_item(mail_item_uuid: str, db: Session = Depends(get_db)):
    return mail_items_crud.get_mail_item(mail_item_uuid, db)


@router.get("/v1/mail_items/", response_model=GenericLimitOffsetPage[MailItem])
@handle_unauthorized
def get_all_mail_items(
    limit: int = 10,
    offset: int = 0,
    ignore_pending: bool = False,
    ignore_complete: bool = False,
    db: Session = Depends(get_db),
):
    return mail_items_crud.get_all_mail_items(db, limit, offset, ignore_pending, ignore_complete)


@router.post("/v1/mail_items/", response_model=MailItem)
@handle_unauthorized
@handle_invalid_mail_item_reference
def create_mail_item(mail_item_create: MailItemCreate, db: Session = Depends(get_db)):
    return mail_items_crud.create_mail_item(mail_item_create, db)


@router.patch("/v1/mail_items/{mail_item_uuid}", response_model=MailItem)
@handle_unauthorized
@handle_mail_item_not_found
@handle_invalid_mail_item_reference
def update_mail_item(
    mail_item_uuid: str, mail_item_update: MailItemUpdate, db: Session = Depends(get_db)
):
    return mail_items_crud.update_mail_item(mail_item_uuid, mail_item_update, db)
