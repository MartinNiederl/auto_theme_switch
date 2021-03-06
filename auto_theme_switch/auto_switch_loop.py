import logging
import sys
import time
from datetime import datetime, timedelta

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

        self.fixed_theme = Theme.AUTO  # Theme option which is set via config or from tray menu.
        self.pending_theme_change = False
        self.previous_date = datetime(1970, 1, 1)  # Only used for logging to print time of sunrise and sunset once per day.
        self.current_theme = None  # Theme which is currently applied. (Only DARK or LIGHT)

    def _get_times(self):
        if self.sun:
            return self.sun.get_local_sunrise_time(), self.sun.get_local_sunset_time()

        return self.config.time_to_switch

    def _get_theme(self, now: datetime):
        """
        Returns the theme which should be applied. If the current time is between the day and night times,
        the theme is DARK, otherwise LIGHT. Never returns AUTO.
        :param now: Current time.
        :return: Theme.DARK or Theme.LIGHT.
        """
        if self.fixed_theme != Theme.AUTO:
            return self.fixed_theme

        start, end = self._get_times()

        if now.date() != self.previous_date:
            self.previous_date = now.date()
            logging.info(f"{self.previous_date} - start: {start.strftime('%H:%M')}, end: {end.strftime('%H:%M')}")

        return Theme.get_matching_theme(start, end, now)

    def _loop(self):
        desktop_no = -1
        previous_loop_time = datetime.now(tz=dateutil.tz.tzlocal())
        while not self.is_stopped:
            try:
                dn = VirtualDesktop.current().number
            except:
                logging.warning("Could not get current desktop number")
                time.sleep(5)
                continue

            # The next lines are required to not miss changing the theme after leaving pc sleep.
            now = datetime.now(tz=dateutil.tz.tzlocal())
            if now - previous_loop_time > timedelta(seconds=30):
                logging.info('Last loop was more than 30 seconds ago, could be after sleep')
                self.pending_theme_change = True

            theme = self._get_theme(now)
            if dn != desktop_no or theme != self.current_theme or self.pending_theme_change:
                desktop_no = dn
                self.pending_theme_change = False
                self.previous_change = now
                self.current_theme = theme

                self.current_theme.apply()

            time.sleep(5)
            previous_loop_time = now

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
        self.fixed_theme = theme
        self.pending_theme_change = True
