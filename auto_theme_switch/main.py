import logging

from auto_theme_switch import tray
from auto_theme_switch.auto_switch_loop import AutoSwitchLoop
from auto_theme_switch.config import config


def main():
    log_enabled, log_path = config.log

    if log_enabled:
        logging.basicConfig(filename=log_path, force=True,
                            filemode='a',
                            format='%(asctime)s [%(levelname)-8s] %(module)s:%(lineno)s - %(message)s',
                            level=logging.INFO)

    logging.info('Starting Auto Theme Switch')
    tray.start()
    AutoSwitchLoop(config).start_loop()


if __name__ == '__main__':
    main()
