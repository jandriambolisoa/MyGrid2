from email.message          import EmailMessage
from email.headerregistry   import Address
import smtplib

from fastapi import APIRouter, status, Depends

from backend.mailings.config import settings as mailings_settings
from backend.mailings.src.sending import exceptions as sending_exceptions
from backend.mailings.src.sending import signals as sending_signals
from backend.mailings.src.sending.schemas import EmailDatas
from backend.mailings.src.templates.dependencies import valid_template_name
from backend.mailings.src.writing.router import write_email

router = APIRouter(
    prefix="/sending",
    tags= ["sending"]
)

@router.post("/{template_name}", status_code=status.HTTP_201_CREATED)
async def send_email(datas: EmailDatas, template_name: str = Depends(valid_template_name), language: str = "en"):
    email = await write_email(datas.fields, template_name, language=language)

    msg = EmailMessage()
    msg['Subject'] = datas.subject
    msg['To'] = datas.receiver
    msg['From'] = Address(mailings_settings.mail_userlabel, mailings_settings.mail_alias, mailings_settings.mail_domain)
    msg.set_content(datas.subject)
    msg.add_alternative(email, subtype="html")

    try:
        with smtplib.SMTP_SSL(mailings_settings.mail_host, mailings_settings.mail_port) as server:
            server.login(mailings_settings.mail_login, mailings_settings.mail_password)
            server.send_message(msg)
        sending_signals.sent.send()
    except smtplib.SMTPAuthenticationError:
        raise sending_exceptions.EmailAuthenticationException(language=language)
