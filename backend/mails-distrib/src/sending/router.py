import os
from email.message          import EmailMessage
from email.headerregistry   import Address
import smtplib

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import HTMLResponse

from .schemas import EmailDatas
from ...config import settings
from ..templates.contents import get_contents_folder
from ..templates.dependencies import valid_template_name
from .exceptions import EmailAuthenticationException

router = APIRouter(
    prefix="/sending",
    tags= ["sending"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def send_email(datas: EmailDatas, language: str = "en"):
    msg = EmailMessage()
    msg['Subject'] = datas.subject
    msg['To'] = datas.receiver
    msg['From'] = Address(settings.mail_userlabel, settings.mail_alias, settings.mail_domain)
    msg.set_content(datas.subject, type="txt")
    msg.add_alternative(datas.content, subtype="html")

    #TODO : logs
    try:
        with smtplib.SMTP_SSL(settings.mail_host, settings.mail_port) as server:
            server.login(settings.mail_login, settings.mail_password)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        raise EmailAuthenticationException(language=language)
