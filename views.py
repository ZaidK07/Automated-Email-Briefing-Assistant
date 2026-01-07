from flask import request
from flask_restful import Resource
from utils import *
import time

MAIN_API_SLEEP_TIME = 5 # this time is in seconds
platform = "whatsapp"

class MainAPI(Resource):
    def get(self):
        while True:
            try:
                new_mail_list, attachment_list = read_new_mails()

                if len(attachment_list) == 0:
                    attachment_list = None

                print("New messages:",len(new_mail_list))
                if len(new_mail_list) > 0:
                    summary_of_emails = summarise_email_list(emails_list=new_mail_list,attachment_list=attachment_list)

                    if platform == "slack":
                        message_status = forward_to_slack_channel(content=summary_of_emails)

                    if platform == "whatsapp":
                        message_status = forward_to_whatsapp(message=summary_of_emails)

                    if message_status == True:
                        print(f'Message sent to {platform} successfully!')
                    else:
                        print('An error occurred while sending message!')

            except Exception as e:
                print('---------------\n',e)

            time.sleep(MAIN_API_SLEEP_TIME)
        return True