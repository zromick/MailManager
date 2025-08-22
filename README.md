# Mail Manager

Problem: Clients with pending issues will not get their mail sent to them.

Solution: Email clients on an interval about pending issues until all issues are marked as complete.

Technologies used: Python, FastAPI, SQLite, SendGrid, React, TypeScript, MUI

## What You'll See:
- Watch the notifier terminal (PORT 8001) to see updates second by second.
- Every 30 seconds, you'll get an email with a list of PENDING mail items.
- Every time an email item is marked COMPLETE, you'll get an email for that, too!
- Watch the UI (PORT 5173) for paginated updates.
- Click a row to mark an item as "COMPLETE."

## Product Overview

*   **mail_manager**: Central database for mail items; handles creation, retrieval, updates.

*   **mail_manager_sdk**: Client library for other services (e.g. `notifier`) to easily talk to `mail_manager`.

*   **notifier**: Polls for mail status from `mail_manager` and sends email alerts based on "PENDING" or "COMPLETE" status.

*   **app_common**: Shared utilities, enums, and data models for all services.

## Setup and Running Instructions

To get both services up and running locally, follow these steps:

### Prerequisites

1. Ensure you have the following installed:

- **Python >= 3.11.11**
- **Node.js >= 20.19.3**
- **NPM >= 10.8.2**
- **PDM >= 2.24.2** (Python Dependency Manager) - Manages dependencies much like NPM for Node.js. If you don't have it, install it globally:
```bash
pip install pdm

Or, if you prefer pipx:
pipx install pdm
```

2. **SendGrid Account**:
You'll need a SendGrid account to send email notifications from the notifier service.
Sign up at SendGrid.com and complete these steps:
- Generate an API Key and set it in backend/notifier/notifier/.env as `NOTIFIER_SENDGRID_API_KEY=your_api_key`
- Verify a sender: https://app.sendgrid.com/settings/sender_auth
- You may receive a 401 if you send over 100 emails per day on the free account

3. Install project dependencies using PDM.

This will also create a virtual environment (.venv) and generate pdm.lock for each.

- Run `pdm install` in each of these directories in order:

```
cd backend/app_common/app_common
cd backend/mail_manager/mail_manager
cd backend/mail_manager/mail_manager_sdk
cd backend/notifier/notifier
```

4. Start the `mail_manager` server:

`cd backend/mail_manager/mail_manager`
`pdm run start`

This will start the server on http://0.0.0.0:8000.

5. Start the `notifier` server in a separate terminal:

`cd backend/notifier/notifier`
`pdm run start`

This will start the server on http://0.0.0.0:8001.

6. Change this variable to your personal email (email might go to spam):

In backend/notifier/notifier/src/notifier/settings.py:
`SENDER_EMAIL: str = "your_personal_email"`

7. Download Insomnia or another API development platform.

You can import backend/Insomnia_2025-07-10.yaml (located at same level as this README.md) and start using the GET, GET all, POST, and PATCH requests I've created.

8. To test back-end:

- Send a POST request with the body below and watch the notifier terminal to see updates. (e.g., POST http://localhost:8000/v1/mail_items/).

```
{
  "mail_item_created_by": "your_personal_email"
}
```

- Send a PATCH request with the UUID of your mail item and the body below. (e.g., PATCH http://localhost:8000/v1/mail_items/{uuid}).

```
{
  "mail_item_review_status": "COMPLETE"
}
```

9. To run the front-end:

- Change `DEFAULT_SENDER_EMAIL` to your personal email.
- Run the following commmands:

```
yarn install
yarn dev
```

## Ideas for back-end updates:
- Add "mail_item_description" field
- Grouped notifications for PENDING items and COMPLETE items
- Slack / UI webhook integration
- Automated end-to-end testing as part of the production pipeline

## Ideas for front-end updates:
- Clean up TS uses of "any"
- Implement sorting / filtering / search on table
- Interval refresh with current page params (offset, limit) from Redux state
- Implement snackbars for notifications

## Other ideas for updates:
- Security implementation
- App running in a Docker image in Kubernetes
