
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate

from user_registration.core.config import settings, logger


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> bool:
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=("user_registration", "user_registration@testemail.com"),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.FAKESMTP_AUTHENTICATION_USERNAME:
        smtp_options["user"] = settings.FAKESMTP_AUTHENTICATION_USERNAME
    if settings.FAKESMTP_AUTHENTICATION_PASSWORD:
        smtp_options["password"] = settings.FAKESMTP_AUTHENTICATION_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logger.info(f"send email result: {response}")
    return response.success
