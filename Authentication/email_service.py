import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ============================================================
# GMAIL CONFIGURATION
# ============================================================

SMTP_HOST = "smtp.gmail.com"

SMTP_PORT = 587

SMTP_EMAIL = os.getenv(
    "SMTP_EMAIL"
)

SMTP_APP_PASSWORD = os.getenv(
    "SMTP_APP_PASSWORD"
)


# ============================================================
# SEND PASSWORD RESET EMAIL
# ============================================================

def send_password_reset_email(
    recipient_email: str,
    reset_token: str
):

    if not SMTP_EMAIL:

        raise RuntimeError(
            "SMTP_EMAIL is not configured."
        )

    if not SMTP_APP_PASSWORD:

        raise RuntimeError(
            "SMTP_APP_PASSWORD is not configured."
        )

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    message = MIMEMultipart()

    message["From"] = SMTP_EMAIL

    message["To"] = recipient_email

    message["Subject"] = "Project Hub - Password Reset"

    body = f"""
Hello,

You requested to reset your Project Hub password.

Your password reset token is:

{reset_token}

Open the Project Hub Forgot Password page and paste this
token into the Reset Token field.

This token is valid for 15 minutes.

If you did not request a password reset, you can safely
ignore this email.

Regards,
Project Hub
"""

    message.attach(
        MIMEText(
            body,
            "plain"
        )
    )

    # --------------------------------------------------------
    # CONNECT TO GMAIL
    # --------------------------------------------------------

    with smtplib.SMTP(
        SMTP_HOST,
        SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            SMTP_EMAIL,
            SMTP_APP_PASSWORD
        )

        server.sendmail(
            SMTP_EMAIL,
            recipient_email,
            message.as_string()
        )