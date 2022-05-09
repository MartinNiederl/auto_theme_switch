from __future__ import annotations

import logging
from datetime import datetime, time
from enum import Enum

from auto_theme_switch import utils
from auto_theme_switch.config import Config

config = Config('config.json')

REG_KEY = r'HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'


class Theme(Enum):
    DARK = (0, config.dark_wallpaper)
    LIGHT = (1, config.light_wallpaper)
    AUTO = (2, None)

    @staticmethod
    def get_matching_theme(start: datetime | time, end: datetime | time, now: datetime):
        if type(start) == datetime and type(end) == datetime:
            return Theme.LIGHT if start <= now <= end else Theme.DARK
        elif type(start) == time and type(end) == time:
            return Theme.LIGHT if start <= now.time() <= end else Theme.DARK

    def apply(self):
        if self.value[0] == 2:
            return

        logging.info(f'Applying theme {self.name}')

        utils.set_registry_value(REG_KEY, 'AppsUseLightTheme', str(self.value[0]))
        utils.set_registry_value(REG_KEY, 'SystemUsesLightTheme', str(self.value[0]))
        if self.value[1]:
            utils.set_wallpaper(self.value[1])
