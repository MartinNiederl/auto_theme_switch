from __future__ import annotations

import logging

import pystray
from PIL import Image
from pystray import Menu, MenuItem

from auto_theme_switch import utils
from auto_theme_switch.auto_switch_loop import AutoSwitchLoop
from auto_theme_switch.theme import Theme

state_theme: Theme = Theme.AUTO
asl = AutoSwitchLoop()


def _on_close(icon: pystray.Icon):
    logging.info('Stopping Auto Theme Switch')
    icon.stop()
    asl.stop_loop()


def _handle_state_change(state: Theme):
    global state_theme
    state_theme = state

    logging.info(f'Theme changed to {state}')

    asl.set_theme(state_theme)


def _set_state(v: Theme):
    def inner(icon, item):
        global state_theme
        state_theme = v

        _handle_state_change(v)

    return inner


def _get_state(v: Theme):
    return lambda item: state_theme == v


def _open_log_dir():
    dir_path = utils.get_current_directory()
    utils.open_directory(dir_path)


def start():
    image = Image.open('icon.png')
    # image = ICOImage('icon_slim.png')

    icon = pystray.Icon(
        'Auto Theme Switch',
        icon=image,
        menu=Menu(
            MenuItem('Force Light', _set_state(Theme.LIGHT), radio=True, checked=_get_state(Theme.LIGHT)),
            MenuItem('Force Dark', _set_state(Theme.DARK), radio=True, checked=_get_state(Theme.DARK)),
            MenuItem('Automatic', _set_state(Theme.AUTO), radio=True, checked=_get_state(Theme.AUTO)),
            Menu.SEPARATOR,
            MenuItem('Open Log Directory', _open_log_dir),
            Menu.SEPARATOR,
            MenuItem('Close', _on_close),
        )
    )

    icon.run_detached()
