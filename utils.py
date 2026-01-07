from simplegmail import Gmail
from google import genai
import os
from prompts import *
import requests
import json
import time

os.makedirs("./attachments",exist_ok=True)
os.makedirs("./gmail_credentials",exist_ok=True)

GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

genai_client = genai.Client(api_key = GOOGLE_GENAI_API_KEY)
genai_model = os.getenv("MODEL_ID")

client_secret_file_path = "./gmail_credentials/client_secret.json"


def read_new_mails():
    gmail_client = Gmail(
        client_secret_file=client_secret_file_path,
        creds_file="./gmail_credentials/zaidk.dev@gmail.json"
    )
    messages = gmail_client.get_unread_inbox()
    # messages = gmail_client.get_messages()

    messages_list = []
    attachment_list = []

    for message in messages:
        message.mark_as_read()

        if message.attachments:
            for attachment in message.attachments:
                attachment_path = f"./attachments/{attachment.filename}"
                attachment.save(attachment_path,overwrite=True)
                attachment_list.append({
                    'attachment_path': attachment_path
                })

        messages_list.append({
            'sender': message.sender,
            'subject_line': message.subject,
            'body': message.plain
        })

    return messages_list, attachment_list


def summarise_email_list(emails_list, attachment_list = None):
    model_prompt = get_summarise_email_list_prompt(email_list=emails_list)

    if attachment_list == None:
        response = genai_client.models.generate_content(
            model = genai_model,
            contents = model_prompt
        )

    else:
        uploaded_files = []

        for attachment in attachment_list:
            file_path = attachment['attachment_path']
            uploaded = genai_client.files.upload(file=file_path)
            uploaded_files.append(uploaded)

        parts = []
        parts.append({"text": "Please summarize the content of the following files and integrate it with the email summary requested below."})
        for file in uploaded_files:
            parts.append({"file_data": {"file_uri": file.uri, "mime_type": file.mime_type}})
        # parts.append({"text": get_summarise_email_list_prompt(email_list=emails_list)})

        parts.append({"text": model_prompt})
        # print(parts)

        for try_count in range(3):
            try:
                response = genai_client.models.generate_content(
                    model=genai_model,
                    contents=json.dumps([{"role": "user", "parts": parts}])
                )
                break
            except Exception as e:
                time.sleep(5)
                print("Error in gemini api call!\n",e)

    return response.text


def forward_to_slack_channel(content):
    payload = {
        "text": content,
        "username": "Email-Summary-Bot"
    }

    response = requests.post(
        SLACK_WEBHOOK_URL, data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        return True
    else:
        return False


def forward_to_whatsapp(message):
    WHATSAPP_URL = os.getenv("WHATSAPP_URL")
    AUTHORIZATION_HEADER = os.getenv("AUTHORIZATION_HEADER")
    WHATSAPP_PHONE_NO = os.getenv("WHATSAPP_PHONE_NO")

    headers = {
        "Authorization": AUTHORIZATION_HEADER,
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_PHONE_NO,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(WHATSAPP_URL, headers=headers, json=payload)

    if response.json().get("messaging_product") == 'whatsapp':
        return True
    else:
        return False