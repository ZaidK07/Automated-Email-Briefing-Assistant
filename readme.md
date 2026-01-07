# Automated Email Briefing Assistant

An intelligent background assistant that monitors your Gmail inbox, generates human-like summaries using Google's Gemini AI, and delivers briefings directly to Slack or WhatsApp.

## 🚀 Features

*   **Smart Summarization:** Uses **Gemini 2.5 Flash** to create concise, executive-style briefings.
*   **Attachment Analysis:** Downloads and incorporates context from email attachments into the summary.
*   **Multi-Platform Delivery:** Supports notifications via **Slack Webhooks** and **WhatsApp API**.
*   **Continuous Monitoring:** Automatically polls for and processes new unread emails.

## 🛠️ Tech Stack

*   **Language:** Python 3
*   **AI Model:** Google Gemini 1.5/2.5 Flash (`google-genai`)
*   **Email:** Gmail API (`simplegmail`)
*   **Backend:** Flask / Flask-RESTful

## ⚙️ Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Automated-Email-Briefing-Assistant
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_GENAI_API_KEY=your_gemini_api_key
    SLACK_WEBHOOK_URL=your_slack_webhook_url
    # Optional: For WhatsApp support
    WHATSAPP_URL=your_whatsapp_url
    AUTHORIZATION_HEADER=your_auth_token
    WHATSAPP_PHONE_NO=target_phone_number
    ```

4.  **Gmail Credentials:**
    *   Enable the Gmail API in your Google Cloud Console.
    *   Download your OAuth `client_secret.json`.
    *   Place it in: `gmail_credentials/client_secret.json`.

## 🏃 Usage

Run the application:
```bash
python app.py
```
*On the first run, a browser window will open to authenticate your Google account.*
