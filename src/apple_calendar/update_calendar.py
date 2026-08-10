import logging
import caldav
from datetime import datetime
from datetime import timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    
)
logger = logging.getLogger(__name__)

class AppleCalendar:
    def __init__(
        self,
        apple_id: str,
        app_password: str,
    ) -> None:
        self.apple_id = apple_id
        self.app_password = app_password

        self.client = caldav.DAVClient(
            url="https://caldav.icloud.com",
            username=self.apple_id,
            password=self.app_password,
        )

        self.principal = self.client.principal()


    def get_calendars(self):
        logger.info("Fetching calendars from Apple Calendar for account: %s", self.apple_id)
        return self.principal.calendars()

    def get_events(self,calendar_name: str | None = None,days: int = 7,):
        start = datetime.now()
        end = start + timedelta(days=days)

        calendars = self.get_calendars()

        if calendar_name:
            calendar = next(
                (
                    cal
                    for cal in calendars
                    if cal.get_display_name().lower() == calendar_name.lower()
                ),
                None,
            )

            if calendar is None:
                raise ValueError(
                    f"Calendar '{calendar_name}' not found"
                )

            return calendar.search(
                start=start,
                end=end,
                event=True,
                expand=True,
            )

        events = []

        for calendar in calendars:
            events.extend(
                calendar.search(
                    start=start,
                    end=end,
                    event=True,
                    expand=True,
                )
            )

        return events

    def create_event(
    self,
    calendar_name: str,
    title: str,
    start: datetime,
    end: datetime,
    description: str | None = None,
) -> None:
        logger.info(f"Creating event '{title}' in calendar '{calendar_name}' from {start} to {end}")
        calendars = self.get_calendars()

        calendar = next(
            (
                cal
                for cal in calendars
                if cal.get_display_name().lower() == calendar_name.lower()
            ),
            None,
        )

        if calendar is None:
            raise ValueError(
                f"Calendar '{calendar_name}' not found"
            )

        if end <= start:
            raise ValueError("Event end time must be after start time")

        logger.info(f"Event '{title}' is valid and will be created")
        calendar.save_event(
            summary=title,
            dtstart=start,
            dtend=end,
            description=description or "",
        )
        logger.info(f"Event '{title}' created successfully in calendar '{calendar_name}'")