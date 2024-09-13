import os
from flask import Flask, request, jsonify
import datetime
import gspread
import json
import logging
from google.oauth2.service_account import Credentials
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
# NOTE: if you are using Railway, you will need to set the environment variables in the Railway dashboard. 
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")

# Debugging: Log the environment variables
app.logger.info(f"SLACK_TOKEN: {'Set' if SLACK_TOKEN else 'Not Set'}")
app.logger.info(f"GOOGLE_CREDENTIALS_JSON: {'Set' if GOOGLE_CREDENTIALS_JSON else 'Not Set'}")

# Check if environment variables are set
if not SLACK_TOKEN or not GOOGLE_CREDENTIALS_JSON:
    app.logger.error("Required environment variables are not set: SLACK_BOT_TOKEN or GOOGLE_CREDENTIALS_JSON")
    raise EnvironmentError("Required environment variables are not set: SLACK_BOT_TOKEN or GOOGLE_CREDENTIALS_JSON")

# Initialize Slack client
slack_client = WebClient(token=SLACK_TOKEN)

# Google Sheets setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_info(
    json.loads(GOOGLE_CREDENTIALS_JSON),
    scopes=SCOPES
)

# Log the authorized scopes for debugging
app.logger.info(f"Authorized scopes: {creds.scopes}")

client = gspread.authorize(creds)

# Replace 'ChangeRequests' with the actual Sheet ID
# Set the sheet ID as a variable
#  https://docs.google.com/spreadsheets/d/YOUR-SHEET-ID/edit?usp=sharing
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1  # Access the first sheet in the Google Sheet by ID

@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())

@app.route('/')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/changereq', methods=['POST'])
def handle_command():
    data = request.form
    trigger_id = data.get("trigger_id")  # Get the trigger ID to open the modal
    app.logger.info(f"Received slash command data: {data}")

    try:
        # Open the modal form
        response = slack_client.views_open(
            trigger_id=trigger_id,
            view={
                "type": "modal",
                "callback_id": "change_request_form",
                "title": {"type": "plain_text", "text": "Change Request Form"},
                "submit": {"type": "plain_text", "text": "Submit"},  # Add submit button
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "company_name",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "company_input"
                        },
                        "label": {"type": "plain_text", "text": "Company Name"}
                    },
                    {
                        "type": "input",
                        "block_id": "license_type",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "license_input"
                        },
                        "label": {"type": "plain_text", "text": "License Type"}
                    },
                    {
                        "type": "input",
                        "block_id": "quantity",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "quantity_input"
                        },
                        "label": {"type": "plain_text", "text": "Quantity"}
                    }
                ]
            }
        )
        app.logger.info(f"Modal opened successfully: {response}")

    except SlackApiError as e:
        app.logger.error(f"Slack API Error: {e.response['error']}")
        return jsonify({"error": f"Slack API Error: {str(e)}"}), 400

    return jsonify({"response": "Modal opened successfully."})

@app.route('/slack/interactivity', methods=['POST'])
def handle_interactivity():
    payload = json.loads(request.form.get("payload"))
    app.logger.info(f"Received interactivity payload: {payload}")
    
    if payload['type'] == 'view_submission':
        user_id = payload['user']['id']
        company_name = payload['view']['state']['values']['company_name']['company_input']['value']
        license_type = payload['view']['state']['values']['license_type']['license_input']['value']
        quantity = payload['view']['state']['values']['quantity']['quantity_input']['value']

        app.logger.info(f"Form submitted with: {company_name}, {license_type}, {quantity}")

        try:
            # Generate CORID
            today = datetime.datetime.now().strftime("%m%d%y")
            records = sheet.get_all_records()
            count = sum(1 for record in records if record['CORID'].startswith(today)) + 1
            corid = f"{today}-{count:02d}"

            # Append to Google Sheet
            sheet.append_row([corid, user_id, company_name, license_type, quantity])
            app.logger.info("Successfully added data to Google Sheet.")

            # Notify in Slack
            slack_client.chat_postMessage(
                channel='C07M2RXFQ9K',  # Replace with your actual Slack channel
                text=f"*New Change Request:*\n*CORID:* {corid}\n*Company:* {company_name}\n*License:* {license_type}\n*Quantity:* {quantity}",
                link_names=True
            )
            app.logger.info("Successfully sent message to Slack channel.")

            # Return an empty response to close the modal
            return jsonify({})

        except Exception as e:
            app.logger.error(f"Error processing form submission: {str(e)}")
            # Return an acknowledgment response to close the modal, but also send an error message
            slack_client.chat_postEphemeral(
                channel=payload['user']['id'],
                user=payload['user']['id'],
                text="An error occurred while processing your request. The form data may have been submitted. Please check and try again if necessary."
            )
            return jsonify({})

    return jsonify({"response": "No action taken."})

if __name__ == '__main__':
    app.run(debug=False)