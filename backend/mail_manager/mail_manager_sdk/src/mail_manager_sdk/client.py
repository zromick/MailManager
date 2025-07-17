import requests
from app_common.schemas import MailItem, MailItemUpdate
from mail_manager_sdk.exceptions import (
    handle_http_errors,
    handle_mail_manager_not_found,
    handle_request_errors,
)


class MailManagerClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @handle_request_errors
    @handle_http_errors
    @handle_mail_manager_not_found
    def create_mail_item(self, mail_item_parameters: dict) -> MailItem:
        response = requests.post(
            f"{self.base_url}/v1/mail_items", json=mail_item_parameters
        ).json()
        return MailItem(**response)

    @handle_request_errors
    @handle_http_errors
    @handle_mail_manager_not_found
    def get_mail_item(self, mail_item_uuid: str) -> MailItem:
        response = requests.get(
            f"{self.base_url}/v1/mail_items/{mail_item_uuid}"
        ).json()
        return MailItem(**response)

    @handle_request_errors
    @handle_http_errors
    def get_all_mail_items(self) -> list[MailItem]:
        response = requests.get(f"{self.base_url}/v1/mail_items")
        response.raise_for_status()
        response_data = response.json()
        return [MailItem.model_validate(item) for item in response_data["items"]]

    @handle_request_errors
    @handle_http_errors
    @handle_mail_manager_not_found
    def update_mail_item(
        self, mail_item_uuid: str, updates: MailItemUpdate
    ) -> MailItem:
        response = requests.patch(
            f"{self.base_url}/v1/mail_items/{mail_item_uuid}",
            json=updates.model_dump(
                exclude_unset=True
            ),  # Use exclude_unset=True for partial updates
        )
        response.raise_for_status()
        json = response.json()
        return MailItem(**json)
