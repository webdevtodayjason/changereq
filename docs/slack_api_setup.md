# Slack API Setup for ChangeReq

This guide provides step-by-step instructions to set up and configure a Slack App for the **ChangeReq** project. The application integrates with Slack to receive slash commands and interact with users through modals, enabling seamless change request submissions.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Create a Slack App](#step-1-create-a-slack-app)
- [Step 2: Configure OAuth & Permissions](#step-2-configure-oauth--permissions)
- [Step 3: Set Up Slash Commands](#step-3-set-up-slash-commands)
- [Step 4: Enable Interactivity](#step-4-enable-interactivity)
- [Step 5: Install the App to Your Workspace](#step-5-install-the-app-to-your-workspace)
- [Step 6: Obtain Necessary Credentials](#step-6-obtain-necessary-credentials)
- [Step 7: Configure the Application with Slack Credentials](#step-7-configure-the-application-with-slack-credentials)
- [Step 8: Verify the Setup](#step-8-verify-the-setup)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

---

## Prerequisites

Before you begin, ensure you have the following:

- **Slack Workspace:** Administrative access to create and manage Slack Apps.
- **GitHub Repository:** Access to the [ChangeReq](https://github.com/webdevtodayjason/changereq.git) repository.
- **Python Environment:** Set up as per the [README.md](./README.md).
- **Railway Account:** To deploy the application ([Sign up here](https://railway.app/)).

---

## Step 1: Create a Slack App

### 1. Access Slack API

- Navigate to the [Slack API](https://api.slack.com/) website.
- Click on **"Your Apps"** in the top-right corner.
- If prompted, sign in with your Slack workspace credentials.

### 2. Create a New App

1. **Click on "Create New App":**
   - Select **"From scratch"**.

2. **App Details:**
   - **App Name:** Enter `ChangeReq`.
   - **Development Slack Workspace:** Select the workspace where you want to install the app.
   - Click **"Create App"**.

---

## Step 2: Configure OAuth & Permissions

### 1. Navigate to OAuth & Permissions

- In your app's dashboard, click on **"OAuth & Permissions"** in the left sidebar.

### 2. Set Redirect URLs

- Under **"Redirect URLs"**, add the following URL:
  - `https://your-app-url/slack/interactivity`

- **Note:** Replace `https://your-app-url` with your actual Railway deployment URL.

- Click **"Add"**.
- Click **"Save URLs"**.

### 3. Assign Scopes

Under **"Scopes"**, assign the following **Bot Token Scopes**:

- `commands`: Allows your app to create and manage slash commands.
- `chat:write`: Enables your app to send messages as the app.
- `chat:write.public`: Allows your app to send messages to channels without joining them.
- `channels:read`: Enables reading basic information about public channels in a workspace.
- `groups:read`: Enables reading basic information about private channels (groups).
- `im:read`: Allows reading basic information about direct message channels.
- `mpim:read`: Allows reading basic information about multiparty direct message channels.

### 4. Save Changes

- After adding the scopes, scroll up and click **"Save Changes"**.

---

## Step 3: Set Up Slash Commands

### 1. Navigate to Slash Commands

- In the left sidebar, click on **"Slash Commands"** under the **"Features"** section.

### 2. Create a New Slash Command

1. **Click on "Create New Command":**

2. **Command Details:**

 - **Command:** `/changereq`
 - **Request URL:** `https://your-app-url/changereq`
   - **Note:** Replace `https://your-app-url` with your actual Railway deployment URL.
 - **Short Description:** `Submit a change request`
 - **Usage Hint:** `[company name] [license type] [quantity]`
 - **Escape Channels, Users, and Links:** **Checked**
 
3. **Click "Save"**.

---

## Step 4: Enable Interactivity

### 1. Navigate to Interactivity & Shortcuts

- In the left sidebar, click on **"Interactivity & Shortcuts"** under the **"Features"** section.

### 2. Enable Interactivity

- Toggle **"Interactivity"** to **"On"**.

### 3. Set Request URL

- **Request URL:** `https://your-app-url/slack/interactivity`
- **Note:** Replace `https://your-app-url` with your actual Railway deployment URL.

- Click **"Save Changes"**.

---

## Step 5: Install the App to Your Workspace

### 1. Navigate to Install App

- In the left sidebar, click on **"Install App"** under the **"Settings"** section.

### 2. Install the App

- Click on **"Install App to Workspace"**.
- Review the permissions and click **"Allow"**.

---

## Step 6: Obtain Necessary Credentials

### 1. Bot User OAuth Token

- After installation, you'll be redirected to the **"OAuth & Permissions"** page.
- **Bot User OAuth Token:** Copy the token starting with `xoxb-`.
- **Example:** `xoxb-123456789012-ABCDEFGHIJKLMN`

### 2. Signing Secret

- Navigate to **"Basic Information"** in the left sidebar.
- Scroll down to **"App Credentials"**.
- **Signing Secret:** Click **"Show"** and copy the secret.
- **Example:** `8fTt3yKc...`

---

## Step 7: Configure the Application with Slack Credentials

### 1. Store Slack Credentials Securely

- Open your `.env` file in the root directory of your project.

### 2. Add Slack Credentials to `.env`

Add the following lines to your `.env` file:

```env
SLACK_BOT_TOKEN=xoxb-123456789012-ABCDEFGHIJKLMN  # Replace with your actual Bot User OAuth Token
SLACK_SIGNING_SECRET=8fTt3yKc...               # Replace with your actual Signing Secret
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
```
Note:
Replace xoxb-123456789012-ABCDEFGHIJKLMN with your actual Bot User OAuth Token.
Replace 8fTt3yKc... with your actual Signing Secret.
Ensure that the entire JSON content for GOOGLE_CREDENTIALS_JSON is enclosed within single quotes (').

###3. Secure your `.env` file

- Ensure that your '.env' file is listed in your '.gitignore' to prevent committing sensitive information:
``` env
# Environment Variables
.env


---

## Step 8: Verify the Setup

### 1.Activate Virtual Environment

- Activate your virtual environment using the command:
```bash
conda activate changereq
```

### 2. Run the Application

- Start the application using the command:
```bash
gunicorn --config gunicorn-cfg.py wsgi:app
```

### 3. Test Health Check
```bash
curl http://localhost:8080/

```
expected response:
```json
{
  "status": "healthy"
}

```

### 4. Test Slack Intagration


- Use the Slack Slash Command `/changereq` to submit a change request.
- submit a change request.
- verify the request in the Google Sheet.
- verify the request in the Slack channel.

---
## Troubleshooting

- Ensure the `GOOGLE_CREDENTIALS_JSON` environment variable is correctly set.
- Verify the service account has the necessary permissions to access the Google Sheet.
- Check the logs for any errors during the application startup or request processing.
- Ensure the `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET` are correctly set.
- Verify the app is installed in the correct Slack workspace.
---

## Additional Resources

- [Slack API Documentation](https://api.slack.com/docs)
- [Google API Documentation](https://developers.google.com/sheets/api)
- [Python Slack SDK](https://slack.dev/python-slack-sdk/)
- [Railway Documentation](https://railway.app/docs)