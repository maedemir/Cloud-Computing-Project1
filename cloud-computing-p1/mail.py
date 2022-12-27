#-------------- email code --------------
# in this file we have a funtion to send an email
import requests


# get YOUR_DOMAIN_NAME and YOUR_API_KEY from Mailgun dashboard
def send_simple_message(email, subject, text):
    return requests.post(
        f"https://api.mailgun.net/v3/sandbox2d66cdc9de224f4e969450469b3ba503.mailgun.org/messages",
        auth=("api", "86a3ae70aff6efb334b908b122a77fd5-69210cfc-d780ff29"),
        data={"from": "<mailgun@sandbox2d66cdc9de224f4e969450469b3ba503.mailgun.org>",
              "to": [email],
              "subject": subject,
              "text": text})