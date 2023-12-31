import imaplib
import email
from email.parser import BytesParser
from email.policy import default
from datetime import datetime, timedelta


def fetch_parse_mark_seen_emails(username: str, password: str) -> list:
    '''
    Fetches and parses emails for the last day and returns a list of email objects with the following fields: 'From', 'Subject', 'Date', 'Body'
    '''
    # IMAP settings
    host = "imap.gmail.com"

    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(host)
        mail.login(username, password)
        mail.select("inbox")  # Select the mailbox

        # Calculate the date range for today
        today = datetime.now()
        # Format the date as required by IMAP
        today_str = today.strftime("%d-%b-%Y")

        # Calculate the date for tomorrow to include emails received until today midnight
        tomorrow = today + timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%d-%b-%Y")

        # Search for emails received today
        search_criteria = f'(SINCE "{today_str}" BEFORE "{tomorrow_str}")'
        status, email_ids = mail.search(None, search_criteria)

        if status != "OK":
            print(f"Error fetching emails for date {today_str}: {status}")
            return []

        # List to store parsed email objects
        parsed_emails = []

        # Retrieve and parse emails
        for email_id in email_ids[0].split():
            try:
                status, email_data = mail.fetch(
                    email_id, "(RFC822)")  # Fetch the email data

                if status != "OK":
                    print(f"Error fetching email {email_id}: {status}")
                    continue

                msg_bytes = email_data[0][1]  # Extract the email bytes

                # Parse the email bytes into a Message object
                msg = BytesParser(policy=default).parsebytes(msg_bytes)

                # Extract email details
                from_address = msg["From"]
                subject = msg["Subject"]
                date = msg["Date"]
                body = ""

                # Process email parts (text and HTML)
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        charset = part.get_content_charset()
                        text_body = part.get_payload(
                            decode=True).decode(charset)
                        break

                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/html":
                        charset = part.get_content_charset()
                        html_body = part.get_payload(
                            decode=True).decode(charset)
                        break

                # Create an email object and add it to the list
                email_obj = {
                    "From": from_address,
                    "Subject": subject,
                    "Date": date,
                    "Text Body": text_body,
                    "HTML Body": html_body
                }
                parsed_emails.append(email_obj)

                # mail.store(email_id, "+FLAGS", "\\Seen")  # Mark the email as read TODO

            except Exception as e:
                print(f"Error processing email {email_id}: {e}")

        # Logout from the server
        mail.logout()

        return parsed_emails

    except Exception as e:
        print(f"Error connecting to the server: {e}")
        return []
