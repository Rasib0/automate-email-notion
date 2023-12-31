# Usage
from chatbot import parse_email_with_chatbot
from imap_helper import fetch_parse_mark_seen_emails
import json
import os
import time
from notion import create_page_wrapper
from dotenv import load_dotenv
from chatbot_fullmail import parse_fullemail_with_chatbot
load_dotenv()


# https://typhoon-troodon-339.notion.site/2bc241cbe7ab4a88abee8fdbc5a52c98?v=f990720931964f279babf10b019cf061

USERNAME = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_PASSWORD")
API_KEY = os.getenv("OPENAI_API_KEY")

parsed_emails = fetch_parse_mark_seen_emails(USERNAME, PASSWORD)
print("Fetching emails...")
# Now you have a list of parsed email objects received today
counter = 1

for email_obj in parsed_emails:
    print("Email #", counter)
    print("From:", email_obj["From"])
    print("Subject:", email_obj["Subject"])
    print("Date:", email_obj["Date"])
    # print("Body:", email_obj["Text Body"])
    print("-" * 40)
    counter += 1
    print("------------------------------------------")

    if "rasibnadeem101@gmail.com" in email_obj["From"] or "Faizan.Ullah@ptclgroup.com" in email_obj["From"]:
        print("Fetched a relevant email! Now parsing it...")
        # time.sleep(20)

        full_mail = email_obj['Text Body']
        if "Rahimyar Khan" in full_mail:
            content_response_data = parse_fullemail_with_chatbot(
                full_mail, API_KEY)

            '''
             chatbot_input = {
                 "From": email_obj["From"],
                 "Subject": email_obj["Subject"],
                 "Date": email_obj["Date"],
                 "Body": email_obj["Text Body"]
             }
             '''
            chatbot_input = content_response_data

            response_data = parse_email_with_chatbot(chatbot_input, API_KEY)

            print("Email parsed! Now adding to Notion...")
            print("Chatbot Response:", response_data)

            responses = create_page_wrapper(
                response_data, content_response_data)

            for response in responses:
                if response.status_code == 200:
                    print("Added to Notion!")
                else:
                    print("Error adding to Notion!", response.json())
