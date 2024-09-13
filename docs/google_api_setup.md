# Setting Up Google API Access for ChangeReq

This guide provides step-by-step instructions to set up access to the Google APIs required for the **ChangeReq** project. The application utilizes the Google Sheets API to interact with Google Sheets, leveraging JSON credentials provided by Google.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Create a Google Cloud Project](#step-1-create-a-google-cloud-project)
- [Step 2: Enable Required APIs](#step-2-enable-required-apis)
- [Step 3: Create a Service Account](#step-3-create-a-service-account)
- [Step 4: Create and Download JSON Credentials](#step-4-create-and-download-json-credentials)
- [Step 5: Share the Google Sheet with the Service Account](#step-5-share-the-google-sheet-with-the-service-account)
- [Step 6: Configure the Application with JSON Credentials](#step-6-configure-the-application-with-json-credentials)
- [Step 7: Verify the Setup](#step-7-verify-the-setup)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

---

## Prerequisites

Before you begin, ensure you have the following:

- **Google Account:** To access the Google Cloud Platform (GCP).
- **GitHub Repository:** Access to the [ChangeReq](https://github.com/webdevtodayjason/changereq.git) repository.
- **Python Environment:** Set up as per the [README.md](./README.md).
- **Railway Account:** To deploy the application ([Sign up here](https://railway.app/)).

---

## Step 1: Create a Google Cloud Project

### 1. Access Google Cloud Console

- Navigate to [Google Cloud Console](https://console.cloud.google.com/).
- Log in with your Google account.

### 2. Create a New Project

1. **Click on the project dropdown** at the top of the page.
2. **Select "New Project".**
3. **Project Name:** Enter `ChangeReq`.
4. **Billing Account:** Select an existing billing account or set up a new one if prompted.
5. **Location:** Choose an organization if applicable.
6. **Click "Create".**

### 3. Select the Project

- After creation, ensure your new project is selected in the project dropdown.

---

## Step 2: Enable Required APIs

### 1. Navigate to APIs & Services

- In the left sidebar, click **"APIs & Services"** > **"Library"**.

### 2. Enable Google Sheets API

1. In the API Library, search for **"Google Sheets API"**.
2. Click on **"Google Sheets API"**.
3. Click **"Enable"**.

### 3. Enable Google Drive API

1. Similarly, search for **"Google Drive API"**.
2. Click on **"Google Drive API"**.
3. Click **"Enable"**.

---

## Step 3: Create a Service Account

### 1. Navigate to Service Accounts

- Go to **"APIs & Services"** > **"Credentials"**.
- Click on **"Create Credentials"** > **"Service Account"**.

### 2. Set Up Service Account

1. **Service account name:** Enter `change_req_service_account`.
2. **Service account ID:** Auto-generated based on the name.
3. **Description:** *(Optional)* `Service account for ChangeReq application`.
4. Click **"Create and Continue"**.

### 3. Assign Roles

- For this application, specific roles are not necessary as it interacts only with Google Sheets and Drive.
- Click **"Continue"** without selecting any roles.

### 4. Grant Users Access

- Not required for this use case.
- Click **"Done"**.

---

## Step 4: Create and Download JSON Credentials

### 1. Navigate to the Service Account

- In **"APIs & Services"** > **"Credentials"**, locate the `change_req_service_account`.
- Click on the service account name to open its details.

### 2. Create Key

1. Click on the **"Keys"** tab.
2. Click **"Add Key"** > **"Create new key"**.
3. Choose **"JSON"** as the key type.
4. Click **"Create"**.

### 3. Download the JSON File

- A JSON file named something like `change_req_service_account-xxxxxxxxxx.json` will be downloaded to your computer.
- **Important:** Store this file securely. Do **not** commit it to your repository.

---

## Step 5: Share the Google Sheet with the Service Account

### 1. Open Your Google Sheet

- Navigate to the Google Sheet you intend to use with the application (e.g., `Change Requests`).

### 2. Share the Sheet

1. Click the **"Share"** button in the top-right corner.
2. Enter the service account's email address, found in the JSON credentials file (e.g., `change_req_service_account@your-project-id.iam.gserviceaccount.com`).
3. Set the permission to **"Editor"**.
4. Click **"Send"**.

---

## Step 6: Configure the Application with JSON Credentials

### 1. Store the JSON Credentials Securely

- Move the downloaded JSON file to a secure location within your project directory (e.g., `credentials/` folder).
- **Do not** commit this file to your repository.

### 2. Set the `GOOGLE_CREDENTIALS_JSON` Environment Variable

- The application expects the JSON content as a string in the `GOOGLE_CREDENTIALS_JSON` environment variable.
- Open the JSON file in a text editor and copy its entire content.
- Add it to your `.env` file:

```env
SLACK_BOT_TOKEN=your-slack-bot-token
GOOGLE_CREDENTIALS_JSON='{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "change_req_service_account@your-project-id.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/change_req_service_account%40your-project-id.iam.gserviceaccount.com"
}'
PORT=8080

### 3. Secure your .env file

- The `.env` file contains sensitive information such as your Slack bot token and Google credentials.
- **Do not** commit this file to your repository.
- Use environment variables in Railway instead of storing sensitive information in the code.

---

## Step 7: Verify the Setup

- Ensure that the application can access the Google Sheet and that changes are reflected correctly.
- Test the application by submitting a change request through Slack.

### 1. Activate Virtual Environment

```bash
conda activate changereq
```

### 2. Run the Application

```bash
gunicorn --config gunicorn_config.py app:app
```

### 3. Test the Health Check Endpoint

```bash
curl http://localhost:8080/health
```
Expected Response:
```
{
  "status": "ok",
  "message": "Application is running"
}
```

### 4. Test the Slack Integration

- Use the Slack Slash Command `/changereq` to submit a change request.
- submit a change request.
- Ensure the request is processed correctly by checking the Google Sheet.

---

## Troubleshooting

- Ensure the `GOOGLE_CREDENTIALS_JSON` environment variable is correctly set.
- Verify the service account has the necessary permissions to access the Google Sheet.
- Check the logs for any errors during the application startup or request processing.

---
Permissions

- The service account needs to have the following permissions:

```json
{
  "role": "Editor",
  "type": "user",
  "email": "change_req_service_account@your-project-id.iam.gserviceaccount.com"
}

Additional Resources

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Google Drive API Documentation](https://developers.google.com/drive/api)
- [Slack API Documentation](https://api.slack.com/docs)
- [Python Google API Documentation](https://googleapis.dev/python/google-api-core/latest/auth.html)
- [Python Slack API Documentation](https://slack.dev/python-slack-sdk/api-docs/)
- [Railway Documentation](https://railway.app/docs)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
---