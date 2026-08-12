import asyncio
import os
import logging
import aiohttp

from whirlpool.auth import Auth
from whirlpool.appliancesmanager import AppliancesManager
from whirlpool.backendselector import BackendSelector
from whirlpool.types import Brand, Region
from whirlpool.oven import Cavity, CookMode
logger = logging.getLogger(__name__)


class KitchenAidOven:
    def __init__(
        self,
        email: str,
        password: str,
    ) -> None:
        self.email = email
        self.password = password

        self.session: aiohttp.ClientSession | None = None
        self.backend: BackendSelector | None = None
        self.auth: Auth | None = None
        self.manager: AppliancesManager | None = None
        self.oven = None

        logger.info(
            "KitchenAidOven initialized for account %s",
            self._masked_email(),
        )

    def _masked_email(self) -> str:
        if "@" not in self.email:
            return "***"

        local, domain = self.email.split("@", 1)

        if len(local) <= 2:
            masked_local = local[0] + "***"
        else:
            masked_local = local[:2] + "***"

        return f"{masked_local}@{domain}"

    def _ensure_connected(self) -> None:
        if self.oven is None:
            logger.error(
                "Oven operation attempted before connection"
            )
            raise RuntimeError("Oven is not connected")

    @staticmethod
    def fahrenheit_to_celsius(temp_f: float) -> float:
        temp_c = (temp_f - 32) * 5 / 9

        logger.info(
            "Converted temperature %.1f°F -> %.1f°C",
            temp_f,
            temp_c,
        )

        return temp_c

    async def connect(self) -> None:
        logger.info("Connecting to KitchenAid oven")

        try:
            self.session = aiohttp.ClientSession()

            self.backend = BackendSelector(
                brand=Brand.KitchenAid,
                region=Region.US,
            )

            logger.debug(
                "Backend configured: brand=%s region=%s",
                Brand.KitchenAid.name,
                Region.US.name,
            )

            self.auth = Auth(
                backend_selector=self.backend,
                username=self.email,
                password=self.password,
                session=self.session,
            )

            logger.info(
                "Authenticating KitchenAid account %s",
                self._masked_email(),
            )

            await self.auth.do_auth()

            logger.info("KitchenAid authentication successful")

            self.manager = AppliancesManager(
                backend_selector=self.backend,
                auth=self.auth,
                session=self.session,
            )

            logger.info("Fetching KitchenAid appliances")

            success = await self.manager.fetch_appliances()

            if not success:
                logger.warning(
                    "Appliance fetch completed unsuccessfully"
                )

            ovens = self.manager.ovens

            logger.info(
                "Appliance discovery returned %d oven(s)",
                len(ovens),
            )

            if not ovens:
                logger.error("No KitchenAid oven found")
                raise RuntimeError("No KitchenAid oven found")

            self.oven = ovens[0]

            logger.info(
                "Connected to oven '%s' [%s]",
                self.oven.name,
                self.oven.said,
            )

            await self.refresh()

            logger.info(
                "KitchenAid oven connection established successfully"
            )

        except Exception:
            logger.exception(
                "Failed to connect to KitchenAid oven"
            )

            await self.disconnect()

            raise

    async def disconnect(self) -> None:
        logger.info("Disconnecting KitchenAid oven")

        if self.session is None:
            logger.debug(
                "No active KitchenAid session to close"
            )
            return

        try:
            await self.session.close()

            logger.info(
                "KitchenAid session closed successfully"
            )

        except Exception:
            logger.exception(
                "Failed while closing KitchenAid session"
            )
            raise

        finally:
            self.session = None
            self.auth = None
            self.manager = None
            self.oven = None

    async def refresh(self) -> None:
        self._ensure_connected()

        logger.debug(
            "Refreshing oven state for '%s' [%s]",
            self.oven.name,
            self.oven.said,
        )

        try:
            await self.oven.fetch_data()

            logger.debug(
                "Oven state refreshed successfully"
            )

        except Exception:
            logger.exception(
                "Failed to refresh oven state"
            )
            raise

    async def get_status(self) -> dict:
        logger.info("Retrieving KitchenAid oven status")

        await self.refresh()

        status = {
            "name": self.oven.name,
            "online": self.oven.get_online(),
            "state": self.oven.get_cavity_state(),
            "cook_mode": self.oven.get_cook_mode(),
            "temperature_c": self.oven.get_temp(),
            "target_temperature_c": self.oven.get_target_temp(),
            "door_open": self.oven.get_door_opened(),
            "light_on": self.oven.get_light(),
        }

        logger.info(
            (
                "Oven status | online=%s | state=%s | "
                "mode=%s | temp=%s°C | target=%s°C | "
                "door_open=%s | light_on=%s"
            ),
            status["online"],
            status["state"],
            status["cook_mode"],
            status["temperature_c"],
            status["target_temperature_c"],
            status["door_open"],
            status["light_on"],
        )

        return status

    async def set_light(self, on: bool) -> bool:
        self._ensure_connected()

        logger.info(
            "Setting oven light to %s",
            "ON" if on else "OFF",
        )

        try:
            success = await self.oven.set_light(on)

            if success:
                logger.info(
                    "Oven light command succeeded: %s",
                    "ON" if on else "OFF",
                )
            else:
                logger.warning(
                    "Oven light command returned failure"
                )

            return success

        except Exception:
            logger.exception(
                "Failed to set oven light to %s",
                "ON" if on else "OFF",
            )
            raise

    async def preheat(
        self,
        temperature_f: float,
    ) -> bool:
        self._ensure_connected()

        logger.info(
            "Preheat requested: %.1f°F",
            temperature_f,
        )

        if not 170 <= temperature_f <= 550:
            logger.warning(
                "Rejected invalid preheat temperature: %.1f°F",
                temperature_f,
            )

            raise ValueError(
                "Temperature must be between 170°F and 550°F"
            )

        temperature_c = self.fahrenheit_to_celsius(
            temperature_f
        )

        logger.info(
            "Starting oven preheat: %.1f°F / %.1f°C",
            temperature_f,
            temperature_c,
        )

        try:
            success = await self.oven.set_cook(
                target_temp=temperature_c,
                mode=CookMode.Bake,
                cavity=Cavity.Upper,
            )

            if success:
                logger.info(
                    "Preheat command accepted: %.1f°F",
                    temperature_f,
                )
            else:
                logger.warning(
                    "Preheat command returned failure: %.1f°F",
                    temperature_f,
                )

            return success

        except Exception:
            logger.exception(
                "Failed to start preheat at %.1f°F",
                temperature_f,
            )
            raise

    async def stop(self) -> bool:
        self._ensure_connected()

        logger.warning(
            "Stopping active oven cooking operation"
        )

        try:
            success = await self.oven.stop_cook()

            if success:
                logger.info(
                    "Oven stop command succeeded"
                )
            else:
                logger.warning(
                    "Oven stop command returned failure"
                )

            return success

        except Exception:
            logger.exception(
                "Failed to stop oven cooking operation"
            )
            raise