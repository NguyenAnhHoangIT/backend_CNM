from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings
from pathlib import Path
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

async def send_welcome_email(email_to: str, user_name: str):
    html = f"""
    <html>
        <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
            <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
                <div style="margin: 0 auto; width: 90%; text-align: center;">
                    <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">Welcome to CNM Store</h1>
                    <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);">
                        <h3 style="margin-bottom: 100px; font-size: 24px;">Hi {user_name},</h3>
                        <p style="margin-bottom: 30px;">Welcome to CNM Store!</p>
                        <p style="margin-bottom: 30px;">We are excited to have you on board.</p>
                        <a style="display: block; margin: 0 auto; border: none; background-color: rgba(255, 214, 10, 1); color: white; width: 50%; line-height: 24px; padding: 10px; font-size: 24px; border-radius: 10px; cursor: pointer; text-decoration: none;" href="http://localhost:3000/login" target="_blank">
                            Login Now
                        </a>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Welcome to CNM Store",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
