import logging

from auto_theme_switch import tray
from auto_theme_switch.auto_switch_loop import AutoSwitchLoop


def main():
    logging.basicConfig(filename='auto_theme_switch.log',
                        filemode='a',
                        format='%(asctime)s | %(levelname)s | [%(module)s.%(funcName)s:%(lineno)s] %(message)s',
                        level=logging.INFO)

    logging.info('Starting Auto Theme Switch')
    tray.start()
    AutoSwitchLoop().start_loop()


if __name__ == '__main__':
    main()
