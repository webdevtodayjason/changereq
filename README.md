# ChangeReq

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Google API Setup](#google-api-setup)
  - [Slack API Setup](#slack-api-setup)
- [Running the Application Locally](#running-the-application-locally)
- [Deployment with Railway](#deployment-with-railway)
- [Endpoints](#endpoints)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Overview

**ChangeReq** is a **Flask** web application integrated with **Slack** and **Google Sheets**. It allows users to submit change requests via Slack, which are then recorded in a Google Sheet and notified in a designated Slack channel. The application is configured for production using **Gunicorn** and is deployed on **Railway**.

## Features

- **Slack Integration:** Receive slash commands and interact with users through Slack modals.
- **Google Sheets Integration:** Store and manage change requests in a Google Sheet.
- **Health Check Endpoint:** Monitor the application's health status.
- **Logging:** Comprehensive logging for monitoring and debugging.
- **Production-Ready Deployment:** Configured with Gunicorn for handling production workloads.

## Technologies Used

- **Python 3.8+**
- **Flask**
- **Gunicorn**
- **Slack SDK**
- **Google Sheets API (gspread)**
- **Railway**

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)
- **Git**
- **Railway Account** (Sign up at [Railway](https://railway.app/))

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/webdevtodayjason/changereq.git
   cd changereq
   ```

2. **Create a Virtual Environment:**

   ```bash
   conda create -n changereq python=3.12
   conda activate changereq
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
## Configuration
Environment Variables
The application relies on several environment variables for configuration. Ensure these are set before running the application.

SLACK_BOT_TOKEN: Your Slack Bot Token.
GOOGLE_CREDENTIALS_JSON: JSON string of your Google service account credentials.
PORT: (Optional) Port number for the application to listen on. Defaults to 8080.

### Setting Environment Variables Locally
Create a .env file in the root directory of your project and add the following:

4. **Set Up Environment Variables:**

   - Create a `.env` file in the root directory.
   - Add the following environment variables:

   ```bash
   SLACK_BOT_TOKEN=<your_slack_bot_token>
   GOOGLE_CREDENTIALS_JSON=<your_google_credentials_json>
   ```

## Running the Application Locally
To run the application locally, use the following command:

```bash
python app.py
```

## Deployment with Railway

1. **Create a Railway Account:**

   - Sign up at [Railway](https://railway.app/).

2. **Create a New Project:**

   - Click on the "New Project" button.
   - Select "GitHub" as the provider and connect your GitHub account.
   - Find the repository you want to deploy and click on "Connect".

3. **Configure Environment Variables:**

   - Go to the "Variables" tab.
   - Add the following variables:

   ```bash
   SLACK_BOT_TOKEN=<your_slack_bot_token>
   GOOGLE_CREDENTIALS_JSON=<your_google_credentials_json>
   PORT=<your_port_number>
   ```

4. **Deploy the Application:**

   - Click on the "Deploy" button.
   - Railway will build and deploy your application.

5. **Access the Application:**

   - Once deployed, you can access your application at the URL provided by Railway.

## Endpoints

### Health Check

To check the health status of the application, send a GET request to:

```bash
http://<your_railway_url>/health
```

### Slack Slash Command

To submit a change request, send a POST request to:

```bash
http://<your_railway_url>/changereq
```

### Slack Modal Submission

To submit a change request via Slack modal, send a POST request to:

```bash
http://<your_railway_url>/changereq
```

### Slack Modal Submission

To submit a change request via Slack modal, send a POST request to:

```bash
http://<your_railway_url>/changereq
```

## Logging

To submit a change request via Slack modal, send a POST request to:

```bash
http://<your_railway_url>/changereq
```
    