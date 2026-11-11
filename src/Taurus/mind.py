from __future__ import annotations

from typing import Optional
import re
from Taurus.action import (
    TurnOnTVAction,
    OpenAppAction,
    ChangeTVVolumeAction,
    PreheatOvenAction,
)

class Taurus:
    
    def __init__(
        self,
        tv,
        firestick,
        oven,
        thermostat,
        calendar,
        portfolio,
        mail_sender,
    ):
        self.tv = tv
        self.firestick = firestick
        self.oven = oven
        self.thermostat = thermostat
        self.calendar = calendar
        self.portfolio = portfolio
        self.mail_sender = mail_sender
        self.pending_action = None



    def turn_on_tv(self):
        self.tv.power_on()

    def turn_off_tv(self):
        self.tv.connect()
        self.tv.power_off()

    def turn_volume_up(self, amount: int = 1):
        self.tv.connect()
        self.tv.volume_up(amount)

    def turn_volume_down(self, amount: int = 1):
        self.tv.connect()
        self.tv.volume_down(amount)

    def mute_tv(self):
        self.tv.connect()
        self.tv.mute()

    def open_app(self, app_name: str):
        self.firestick.connect()
        self.firestick.start_app_by_name(app_name)

    async def preheat_oven(self, temperature_f: int):
        await self.oven.connect()

        try:
            return await self.oven.preheat(temperature_f)
        finally:
            await self.oven.disconnect()

    async def stop_oven(self):
        await self.oven.connect()

        try:
            return await self.oven.stop()
        finally:
            await self.oven.disconnect()

    def send_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        attachment_paths: Optional[list[str]] = None,
    ):
        return self.mail_sender.send_email(
            recipient_email,
            subject,
            body,
            attachment_paths,
        )

    def get_calendar_events(self):
        return self.calendar.get_events()

    def get_portfolio_value(self):
        return self.portfolio.get_portfolio_value()

    async def handle_command(self, command: str):
        command = command.lower().strip()

        if command == "turn on the tv":
            self.turn_on_tv()
            return "Turning on the TV."

        if command == "turn off the tv":
            self.turn_off_tv()
            return "Turning off the TV."

        if command.startswith("open "):
            app_name = command.removeprefix("open ").strip()
            self.open_app(app_name)
            return f"Opening {app_name}."

        if command.startswith("volume up"):
            match = re.search(r"\d+", command)
            amount = int(match.group()) if match else 1

            self.turn_volume_up(amount)
            return f"Turning volume up by {amount}."

        if command.startswith("volume down"):
            match = re.search(r"\d+", command)
            amount = int(match.group()) if match else 1

            self.turn_volume_down(amount)
            return f"Turning volume down by {amount}."

        if self.pending_action == "preheat_oven":
            match = re.search(r"\d+", command)

            if not match:
                return "What temperature should I preheat the oven to?"

            temperature = int(match.group())
            self.pending_action = None

            await self.preheat_oven(temperature)

            return f"Preheating the oven to {temperature}°F."

        if "preheat oven" in command:
            match = re.search(r"\d+", command)

            if not match:
                self.pending_action = "preheat_oven"
                return "What temperature should I preheat the oven to?"

            temperature = int(match.group())

            await self.preheat_oven(temperature)

            return f"Preheating the oven to {temperature}°F."

    async def execute(self, action):
        if isinstance(action, TurnOnTVAction):
            self.turn_on_tv()

        elif isinstance(action, OpenAppAction):
            self.open_app(action.app_name)

        elif isinstance(action, ChangeTVVolumeAction):
            if action.direction == "up":
                self.turn_volume_up(action.amount)
            else:
                self.turn_volume_down(action.amount)

        elif isinstance(action, PreheatOvenAction):
            await self.preheat_oven(action.temperature_f)

        else:
            raise ValueError(
                f"Unsupported action type: {type(action).__name__}"
            )