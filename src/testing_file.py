import datetime
import logging
import smtplib
from email.message import EmailMessage
import os
from mail_sender.send_mail import MailSender
from apple_calendar.update_calendar import AppleCalendar
from kitchen.oven import KitchenAidOven

import aiohttp
import asyncio
from whirlpool.auth import Auth
from whirlpool.appliancesmanager import AppliancesManager
from whirlpool.backendselector import BackendSelector
from whirlpool.oven import Cavity, CookMode
from whirlpool.types import Brand, Region





logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    
)

logger = logging.getLogger(__name__)

# def main() -> None:
    
#     mail_sender = MailSender(
#         sender_email="ammarogeil@gmail.com",
#         sender_password=os.environ["JARVIS_GMAIL_APP_PASSWORD"],
#     )

#     mail_sender.send_email(
#         recipient_email="ammarogeil@gmail.com",
#         subject="Jarvis First Email",
#         body="This is a test email sent from the MailSender class.",
#         attachment_paths = ["C:\\Users\\ammar\\Downloads\\Laptop nook.png"]
#     )




# def main() -> None:
#     calendar_client = AppleCalendar(
#         apple_id=os.environ["JARVIS_APPLE_ID"],
#         app_password=os.environ["JARVIS_APPLE_APP_PASSWORD"],
#     )

#     calendars = calendar_client.get_calendars()

#     for calendar in calendars:
#         print(calendar.get_display_name())

#     calendar = next(
#         cal
#         for cal in calendars
#         if cal.get_display_name() == "Personal"
#     )

#     for event in calendar_client.get_events(None, days=7):
#         vevent = event.vobject_instance.vevent

#         print("Title:", vevent.summary.value)
#         print("Start:", vevent.dtstart.value)

#         if hasattr(vevent, "dtend"):
#             print("End:", vevent.dtend.value)

#         print()

#     calendar_client.create_event(
#     calendar_name="Personal",
#     title="Jarvis Calendar Test",
#     start=datetime.datetime(2026, 8, 10, 18, 0),
#     end=datetime.datetime(2026, 8, 10, 19, 0),
#     description="Created by Jarvis",
# )

async def main() -> None:
    oven = KitchenAidOven(
        email=os.environ["JARVIS_WHIRLPOOL_EMAIL"],
        password=os.environ["JARVIS_WHIRLPOOL_PASSWORD"],
    )

    try:
        await oven.connect()

        status = await oven.get_status()

        print("Oven:", status["name"])
        print("Online:", status["online"])
        print("State:", status["state"])
        print("Current temp:", status["temperature_c"])
        print("Target temp:", status["target_temperature_c"])

        # success = await oven.stop(True)

        # print("Preheat result:", success)

        await asyncio.sleep(5)

        status = await oven.get_status()

        print("\nAfter command:")
        print("State:", status["state"])
        print("Cook mode:", status["cook_mode"])
        print("Current temp:", status["temperature_c"])
        print("Target temp:", status["target_temperature_c"])

    finally:
        await oven.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

