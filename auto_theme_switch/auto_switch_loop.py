import logging
import sys
import time
from datetime import datetime

import dateutil.tz
from pyvda import VirtualDesktop
from suntime import Sun

from auto_theme_switch import utils
from auto_theme_switch.config import Config
from auto_theme_switch.theme import Theme


class AutoSwitchLoop(metaclass=utils.Singleton):

    def __init__(self, config: Config):
        self.config = config
        self.is_stopped = False

        latitude, longitude = config.location
        if latitude is not None and longitude is not None:
            logging.info(f'Using latitude: {latitude}, longitude: {longitude}')
            self.sun = Sun(latitude, longitude)
        else:
            logging.info('No latitude and longitude set, using config day and night times')

        self.theme = Theme.AUTO
        self.pending_theme_change = False
        self.previous_date = datetime(1970, 1, 1)

    def _get_times(self):
        if self.sun:
            return self.sun.get_local_sunrise_time(), self.sun.get_local_sunset_time()

        return self.config.time_to_switch

    def _get_theme(self):
        if self.theme == Theme.AUTO:
            start, end = self._get_times()

            now = datetime.now(tz=dateutil.tz.tzlocal())

            if now.date() != self.previous_date:
                self.previous_date = now.date()
                logging.info(f"{self.previous_date} - start: {start.strftime('%H:%M')}, end: {end.strftime('%H:%M')}")

            return Theme.get_matching_theme(start, end, now)

        return self.theme

    def _loop(self):
        desktop_no = -1
        while not self.is_stopped:
            try:
                dn = VirtualDesktop.current().number
            except:
                logging.error("Could not get current desktop number")
                continue

            if dn != desktop_no or self.pending_theme_change:
                desktop_no = dn
                self.pending_theme_change = False

                self._get_theme().apply()

            time.sleep(5)

    def start_loop(self):
        logging.info("Starting loop...")
        self.is_stopped = False
        try:
            self._loop()
        except KeyboardInterrupt:
            logging.error(f"Loop terminated by user")
            sys.exit(0)

    def stop_loop(self):
        logging.info("Stopping loop...")
        self.is_stopped = True

    def set_theme(self, theme: Theme):
        self.theme = theme
        self.pending_theme_change = True
