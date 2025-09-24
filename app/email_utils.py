from email.message import EmailMessage
import aiosmtplib

async def send_welcome_email(email_to: str, user_name: str):
    message = EmailMessage()
    message["From"] = "your_email@example.com"
    message["To"] = email_to
    message["Subject"] = "������ �� ���������!"

    message.set_content(
        f"�����, {user_name}!\n\n������, �� �������������� � ������ ��������� �������. "
        "�� ��� ����� ��� � ����� �������!\n\n� �������,\n������� Imperial Grace ??"
    )

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="your_email@example.com",
        password="your_app_password"
    )
