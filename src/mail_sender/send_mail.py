from email import message
import logging
import smtplib
from email.message import EmailMessage
import os
from pathlib import Path
import mimetypes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    
)


logger = logging.getLogger(__name__)
    
class MailSender:
    def __init__(self, sender_email: str, sender_password: str) -> None:
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        attachment_paths: list[str] | None = None,
    ) -> None:

        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.set_content(body)

        if attachment_paths:
            logger.info(f"Adding attachments: {attachment_paths}")
            for attachment_path in attachment_paths:
                path = Path(attachment_path)

                if not path.exists():
                    raise FileNotFoundError(f"Attachment not found: {path}")

                mime_type, _ = mimetypes.guess_type(path)

                if mime_type:
                    maintype, subtype = mime_type.split("/", 1)
                else:
                    maintype = "application"
                    subtype = "octet-stream"

                with path.open("rb") as file:
                    message.add_attachment(
                        file.read(),
                        maintype=maintype,
                        subtype=subtype,
                        filename=path.name,
                    )
    

        try:
            logger.info(f"Sending email to {recipient_email} with subject '{subject}'")
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                logger.info(f"Email sent successfully to {recipient_email} with subject '{subject}'")

        except smtplib.SMTPAuthenticationError as exc:
            raise RuntimeError(
                "Gmail authentication failed. Use a Google app password, "
                "not your normal account password."
            ) from exc

        except smtplib.SMTPException as exc:
            raise RuntimeError(f"Email could not be sent: {exc}") from exc



