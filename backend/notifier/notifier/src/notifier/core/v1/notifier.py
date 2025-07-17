import asyncio
import datetime
from functools import lru_cache

from app_common.enums import MailItemStatus
from app_common.logger import logger
from app_common.schemas import MailItem, MailItemUpdate
from mail_manager_sdk.client import MailManagerClient
from mail_manager_sdk.exceptions import MailManagerClientException
from notifier.core.v1.notifiers.email_notifier import get_email_notifier
from notifier.exceptions import NotifierException
from notifier.settings import settings

# Initialize clients
mail_manager_client = MailManagerClient(settings.MAIL_MANAGER_BASE_URL)


class Notifier:
    def __init__(self):
        self.notifiers = [
            get_email_notifier(),
        ]
        self.polling_task: asyncio.Task | None = None
        self.poll_counter: int = 0

    async def start_polling(self):
        """Starts the continuous polling for mail item review statuses."""
        if self.polling_task is not None and not self.polling_task.done():
            logger.warning("Mail item review polling task is already running.")
            return

        logger.info("Starting mail item review status polling task.")
        self.polling_task = asyncio.create_task(self._poll_mail_item_review_statuses())

    async def _poll_mail_item_review_statuses(self):
        """
        Continuously polls for mail item review statuses and sends notifications.
        Filters out items that have already sent their final notification.
        """
        self.polling_start_time = datetime.datetime.now(datetime.timezone.utc)
        while True:
            self.poll_counter += 1
            try:
                all_mail_items: list[MailItem] = (
                    mail_manager_client.get_all_mail_items()
                )
                current_time = datetime.datetime.now(datetime.timezone.utc)

                # Filter out items that are COMPLETE and have mail_item_final_notification_sent = True
                mail_items_to_process = [
                    item
                    for item in all_mail_items
                    if not (
                        item.mail_item_review_status == MailItemStatus.COMPLETE
                        and item.mail_item_final_notification_sent
                    )
                ]

                mail_item_uuids_in_poll = [
                    item.mail_item_uuid for item in mail_items_to_process
                ]
                logger.info(
                    "Poll {} - Mail Items with Reviews Still Pending: {}",
                    self.poll_counter,
                    mail_item_uuids_in_poll,
                )

                for mail_item in mail_items_to_process:
                    mail_item_uuid = mail_item.mail_item_uuid
                    recipient_email = mail_item.mail_item_created_by

                    if mail_item.mail_item_review_status == MailItemStatus.PENDING:
                        # Send PENDING reminder every X minutes/hours based on polling start time
                        time_since_polling_start = (
                            current_time - self.polling_start_time
                        ).total_seconds()

                        if (
                            time_since_polling_start
                            % settings.MAIL_ITEM_REVIEW_NOTIFICATION_INTERVAL_SECONDS
                        ) < settings.MAIL_ITEM_REVIEW_POLL_INTERVAL_SECONDS:
                            logger.info(
                                "Mail item {} review status is PENDING. Sending reminder notification.",
                                mail_item_uuid,
                            )
                            for notifier in self.notifiers:
                                try:
                                    notifier.send_review_pending_notification(
                                        mail_item_uuid, recipient_email, mail_item
                                    )
                                except NotifierException as e:
                                    logger.exception(
                                        "Error sending review pending notification for {} using {}: {}",
                                        mail_item_uuid,
                                        type(notifier).__name__,
                                        str(e),
                                    )

                    elif mail_item.mail_item_review_status == MailItemStatus.COMPLETE:
                        if not mail_item.mail_item_final_notification_sent:
                            logger.info(
                                "Mail item {} review status is COMPLETE. Sending completion notification.",
                                mail_item_uuid,
                            )
                            for notifier in self.notifiers:
                                try:
                                    notifier.send_review_complete_notification(
                                        mail_item_uuid, recipient_email, mail_item
                                    )
                                    # Mark mail_item_final_notification_sent as True in DB
                                    update_payload = MailItemUpdate(
                                        mail_item_final_notification_sent=True
                                    )
                                    mail_manager_client.update_mail_item(
                                        mail_item_uuid, update_payload
                                    )
                                except NotifierException as e:
                                    logger.exception(
                                        "Error sending review complete notification for {} using {}: {}",
                                        mail_item_uuid,
                                        type(notifier).__name__,
                                        str(e),
                                    )

            except MailManagerClientException as e:
                logger.exception(
                    "MailManager Client raised an exception during mail item review status polling: {}",
                    str(e),
                )
            except Exception as e:
                logger.exception(
                    "An unexpected exception occurred during mail item review polling loop: {}",
                    str(e),
                )

            await asyncio.sleep(settings.MAIL_ITEM_REVIEW_POLL_INTERVAL_SECONDS)


# singleton
@lru_cache(maxsize=1)
def get_notification_manager() -> Notifier:
    return Notifier()
