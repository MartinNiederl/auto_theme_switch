from __future__ import annotations

import json
import os
from datetime import time

from auto_theme_switch import utils


class Config(metaclass=utils.Singleton):
    DEFAULT = {
        "theme": {
            "initial_mode": "auto",
            "time_to_switch": {
                "use": True,
                "day": "08:00",
                "night": "19:00"
            }
        },
        "log": {
            "enabled": True,
            "path": os.path.join(utils.get_current_directory(), 'auto_theme_switch.log')
        }
    }

    def __init__(self, file_path: str):
        self.config = Config.DEFAULT.copy()
        utils.merge_dict(self.config, self._read_config(file_path))

    @staticmethod
    def _read_config(path: str) -> dict:
        if path is None or not os.path.exists(path):
            print(f'Config file not found: {path}')
            return {}

        with open(path, 'r') as f:
            return json.load(f)

    def __str__(self):
        return json.dumps(self.config, indent=4)

    @property
    def _tts(self) -> dict:
        return self.config['theme'].get('time_to_switch')

    @property
    def _l(self) -> dict:
        return self.config['theme'].get('location')

    @property
    def _w(self) -> dict:
        return self.config['theme'].get('wallpaper')

    @property
    def time_to_switch(self) -> tuple[time, time] | tuple[None, None]:
        if self._tts and self._tts.get('use') == True:
            return utils.parse_time_str(self._tts.get('day')), utils.parse_time_str(self._tts.get('night'))
        return None, None

    @property
    def location(self) -> tuple[float, float] | tuple[None, None]:
        if self._l and self._l.get('use') == True:
            return float(self._l.get('latitude', 0)), float(self._l.get('longitude', 0))
        return None, None

    @property
    def light_wallpaper(self) -> str | None:
        if self._w:
            return self._w.get('light')

    @property
    def dark_wallpaper(self) -> str | None:
        if self._w:
            return self._w.get('dark')

    @property
    def wallpapers(self) -> tuple[str, str]:
        return self.light_wallpaper, self.dark_wallpaper

    @property
    def log(self) -> tuple[bool, str]:
        return self.config['log'].get('enabled'), self.config['log'].get('path')


config = Config(utils.get_config_path())
