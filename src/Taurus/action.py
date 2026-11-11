from typing import Literal
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# --------------------
# Television
# --------------------

class TurnOnTVAction(BaseModel):
    action: Literal["turn_on_tv"]


class TurnOffTVAction(BaseModel):
    action: Literal["turn_off_tv"]


class MuteTVAction(BaseModel):
    action: Literal["mute_tv"]


class ChangeTVVolumeAction(BaseModel):
    action: Literal["change_tv_volume"]
    direction: Literal["up", "down"]
    amount: int = Field(default=1, ge=1, le=100)


# --------------------
# Fire Stick
# --------------------

class OpenAppAction(BaseModel):
    action: Literal["open_app"]
    app_name: str


class FireStickNavigationAction(BaseModel):
    action: Literal["firestick_navigation"]
    direction: Literal[
        "up",
        "down",
        "left",
        "right",
        "select",
        "back",
        "home",
    ]


class MediaControlAction(BaseModel):
    action: Literal["media_control"]
    command: Literal[
        "play_pause",
        "next",
        "previous",
    ]


# --------------------
# Oven
# --------------------

class PreheatOvenAction(BaseModel):
    action: Literal["preheat_oven"]
    temperature_f: int = Field(ge=170, le=550)


class StopOvenAction(BaseModel):
    action: Literal["stop_oven"]


class GetOvenStatusAction(BaseModel):
    action: Literal["get_oven_status"]

class OvenLightAction(BaseModel):
    action: Literal["oven_light"]
    state: Literal["on", "off"]


# --------------------
# Calendar
# --------------------

class GetCalendarEventsAction(BaseModel):
    action: Literal["get_calendar_events"]
    calendar_name: str | None = None
    days: int = Field(default=7, ge=1, le=365)


class CreateCalendarEventAction(BaseModel):
    action: Literal["create_calendar_event"]
    calendar_name: str
    title: str
    start: datetime
    end: datetime
    description: str | None = None


# --------------------
# Email
# --------------------

class SendEmailAction(BaseModel):
    action: Literal["send_email"]
    recipient_email: EmailStr
    subject: str
    body: str
    attachment_paths: list[str] | None = None


# --------------------
# Portfolio
# --------------------

class GetPortfolioValueAction(BaseModel):
    action: Literal["get_portfolio_value"]


class GetPositionAction(BaseModel):
    action: Literal["get_position"]
    ticker: str


class GetPortfolioAllocationAction(BaseModel):
    action: Literal["get_portfolio_allocation"]


# --------------------
# Thermostat - later
# --------------------

class SetThermostatTemperatureAction(BaseModel):
    action: Literal["set_thermostat_temperature"]
    temperature_c: float = Field(ge=10, le=30)


class SetThermostatModeAction(BaseModel):
    action: Literal["set_thermostat_mode"]
    mode: Literal["heat", "cool", "auto", "off"]


class SetThermostatFanAction(BaseModel):
    action: Literal["set_thermostat_fan"]
    speed: Literal["auto", "low", "medium", "high"]


TaurusAction = (
    TurnOnTVAction
    | TurnOffTVAction
    | MuteTVAction
    | ChangeTVVolumeAction
    | OpenAppAction
    | FireStickNavigationAction
    | MediaControlAction
    | PreheatOvenAction
    | StopOvenAction
    | GetOvenStatusAction
    | GetCalendarEventsAction
    | CreateCalendarEventAction
    | SendEmailAction
    | GetPortfolioValueAction
    | GetPositionAction
    | GetPortfolioAllocationAction
)