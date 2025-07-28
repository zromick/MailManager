from functools import lru_cache
from http import HTTPStatus

from app_common.logger import logger
from app_common.schemas import MailItem
from email_validator import EmailNotValidError, validate_email
from notifier.core.v1.notifiers.abstract_notifier import AbstractNotifier
from notifier.exceptions import EmailNotificationException, InvalidEmailInputException
from notifier.settings import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def is_company_email(email: str) -> bool:
    """Returns True if the email belongs to the company domain."""
    try:
        v = validate_email(email)
        return v.domain.lower() == "gmail.com"
    except EmailNotValidError as e:
        raise InvalidEmailInputException(
            f"The provided email '{email}' is not valid."
        ) from e


class EmailNotifier(AbstractNotifier):
    def __init__(self):
        self.sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.sender_email = settings.SENDER_EMAIL

    def _send_email(self, subject: str, body: str, recipient_email: str) -> None:
        """Send an email using SendGrid"""
        try:
            message = Mail(
                from_email=self.sender_email,
                to_emails=recipient_email,
                subject=subject,
                html_content=body,
            )

            response = self.sg.send(message)
            if response.status_code != HTTPStatus.ACCEPTED:
                raise EmailNotificationException(
                    f"SendGrid API returned status code {response.status_code}. "
                    f"Response headers: {response.headers}. "
                    f"Response body: {response.body}"
                )

            logger.info("Successfully sent email to {}.", recipient_email)
        except Exception as e:
            logger.exception("Failed to send email to {}", recipient_email)
            raise EmailNotificationException from e

    def send_review_pending_notification(
        self, mail_item_uuid: str, recipient_email: str, mail_item: MailItem
    ):
        """
        Sends an email notification that a mail item is still pending review.
        """
        subject = (
            f"Action Required: Mail Item {mail_item_uuid} Review Status Still Pending"
        )
        body = f"""
			<p>This is a reminder that mail item {mail_item_uuid} has a status of "PENDING".</p>
			<p>It was created by {mail_item.mail_item_created_by} at {mail_item.mail_item_created_time.strftime('%Y-%m-%d %H:%M:%S %Z')}.</p>
		"""
        logger.info(
            "Attempting to send review pending email for mail item {} to {}",
            mail_item_uuid,
            recipient_email,
        )
        self._send_email(subject, body, recipient_email)
        logger.info(
            "Successfully sent review pending email for mail item {} to {}",
            mail_item_uuid,
            recipient_email,
        )

    def send_review_complete_notification(
        self, mail_item_uuid: str, recipient_email: str, mail_item: MailItem
    ):
        """
        Sends an email notification that a mail item's review status is COMPLETE.
        """
        subject = f"Mail Item {mail_item_uuid} Review Complete"
        body = f"""
			<p>This is to inform you that mail item {mail_item_uuid} has been marked as "COMPLETE".</p>
			<p>It was created by {mail_item.mail_item_created_by} at {mail_item.mail_item_created_time.strftime('%Y-%m-%d %H:%M:%S %Z')}.</p>
		"""
        logger.info(
            "Attempting to send review complete email for mail item {} to {}",
            mail_item_uuid,
            recipient_email,
        )
        self._send_email(subject, body, recipient_email)
        logger.info(
            "Successfully sent review complete email for mail item {} to {}",
            mail_item_uuid,
            recipient_email,
        )


# singleton
@lru_cache(maxsize=1)
def get_email_notifier() -> EmailNotifier:
    return EmailNotifier()
