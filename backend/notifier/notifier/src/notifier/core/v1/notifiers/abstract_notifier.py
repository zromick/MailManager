from abc import ABC, abstractmethod

from app_common.schemas import MailItem


class AbstractNotifier(ABC):
    @abstractmethod
    def send_review_pending_notification(
        self, mail_item_uuid: str, recipient_email: str, mail_item: MailItem
    ) -> None:
        pass

    @abstractmethod
    def send_review_complete_notification(
        self, mail_item_uuid: str, recipient_email: str, mail_item: MailItem
    ) -> None:
        pass
