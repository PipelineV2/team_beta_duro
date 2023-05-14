# CREDIT https://medium.com/thelorry-product-tech-data/fastapi-email-service-with-python-boto3-amazon-ses-and-elastic-container-registry-ecr-2c30f8a38722
# The link has more information if more advanced features are needed.
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import ClientError
from jinja2 import Template

from app.core.global_config import app_config
from app.modules.mailer.mailer_exceptions import SendEmailException

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
# ses_client = boto3.client("ses", region_name=app_config.AWS_REGION)


def create_email_multipart_message(
    sender: str,
    sender_name: str,
    recipients: list,
    cc: list,
    bcc: list,
    title: str,
    text: str = None,
    body: str = None,
    attachments: list = None,
) -> MIMEMultipart:
    if text and body:
        # assign subtype - multipart/alternative
        content_subtype = "alternative"
    else:
        # assign subtype - multipart/mixed
        content_subtype = "mixed"

    # Instantiate a MIMEMultipart message object
    message = MIMEMultipart(content_subtype)
    message["Subject"] = title

    # if sender_name is provided, the format will be 'Sender Name <email@example.com>'
    if sender_name is None:
        message["From"] = f"{sender}"
    else:
        message["From"] = f"{sender_name} <{sender}>"

    message["To"] = ", ".join(recipients)
    message["CC"] = ", ".join(cc)
    message["BCC"] = ", ".join(bcc)

    # Record the MIME types of both parts:
    # text - defined as text/plain part
    if text:
        part = MIMEText(text, "plain")
        message.attach(part)
    # body - defined as text/html part
    if body:
        part = MIMEText(body, "html")
        message.attach(part)

    # Add attachments
    for attachment in attachments or []:
        with open(attachment, "rb") as f:
            part = MIMEApplication(f.read())
            part.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(attachment),
            )
            message.attach(part)

    return message


def send_mail_with_template(
    recipients: list, subject: str, template_name: str, template_data: dict = {}
) -> dict:
    file_name = "app/templates/{}.html".format(template_name)
    body = Template(open(file_name, "r").read()).render(template_data)
    return send_mail(recipients, subject, body)


def send_mail(
    recipients: list,
    subject: str,
    body: str,
    *,
    sender: str = app_config.SENDER_EMAIL,
    sender_name: str = app_config.SENDER_NAME,
    cc: list = [],
    bcc: list = [],
    text: str = None,
    attachments: list = None,
) -> dict:
    ...
    # try:
    #     msg = create_email_multipart_message(
    #         sender, sender_name, recipients, cc, bcc, subject, text, body, attachments
    #     )

    #     # All emails in the requests including recipients, cc and bcc list need to be added in the destinations.
    #     destinations = []
    #     destinations.extend(recipients)
    #     destinations.extend(cc)
    #     destinations.extend(bcc)
    #     ses_response = ses_client.send_raw_email(
    #         Source=sender,
    #         Destinations=destinations,
    #         RawMessage={"Data": msg.as_string()},
    #     )

    # except ClientError as e:
    #     raise SendEmailException(
    #         message=e.response["Error"]["Message"], details=str(e.response)
    #     )
    # else:
    #     response = {
    #         "status": True,
    #         "message": "Email Successfully Sent.",
    #         "message_id": ses_response["MessageId"],
    #         "response": ses_response,
    #     }

    #     return response
