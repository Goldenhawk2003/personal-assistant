import os
import asyncio

from dotenv import load_dotenv

from Taurus.mind import Taurus
from Television.samsung import SamsungTV
from Television.firestick import FireStick
from kitchen.oven import KitchenAidOven
from apple_calendar.update_calendar import AppleCalendar
from Finances.read_portfolio import PortfolioReader
from mail_sender.send_mail import MailSender


load_dotenv()


def build_taurus():
    tv = SamsungTV(
        ip=os.environ["JARVIS_SAMSUNG_TV_IP"],
        token=os.environ["JARVIS_SAMSUNG_TV_TOKEN"],
        mac_address=os.environ["JARVIS_SAMSUNG_TV_MAC"],
    )

    firestick = FireStick(
        ip=os.environ["JARVIS_FIRESTICK_IP"],
        adb_path=os.environ["JARVIS_ADB_PATH"],
    )

    oven = KitchenAidOven(
        email=os.environ["JARVIS_WHIRLPOOL_EMAIL"],
        password=os.environ["JARVIS_WHIRLPOOL_PASSWORD"],
    )

    calendar = AppleCalendar(
    apple_id=os.environ["JARVIS_APPLE_ID"],
    app_password=os.environ["JARVIS_APPLE_APP_PASSWORD"],
)

    portfolio = PortfolioReader()

    mail_sender = MailSender(
        sender_email=os.environ["JARVIS_GMAIL_ADDRESS"],
        sender_password=os.environ["JARVIS_GMAIL_APP_PASSWORD"],
    )

    return Taurus(
        tv=tv,
        firestick=firestick,
        oven=oven,
        thermostat=None,
        calendar=calendar,
        portfolio=portfolio,
        mail_sender=mail_sender,
    )