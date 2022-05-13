import collections.abc
import ctypes
import datetime
import os
import winreg


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_wallpaper() -> str:
    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(0x0073, len(ubuf), ubuf, 0)
    return ubuf.value


def set_wallpaper(path: str):
    changed = 1 | 2
    ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, path, changed)


def set_registry_value(key: str, value: str, data: int):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_ALL_ACCESS) as key:
        winreg.SetValueEx(key, value, 0, winreg.REG_DWORD, data)

    # command = ['reg.exe', 'add', key, '/v', value, '/t', 'REG_DWORD', '/d', data, '/f']
    # subprocess.run(command, stdout=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))


def get_config_path():
    return os.path.join(get_current_directory(), 'config.json')


def open_directory(path: str):
    if os.path.isdir(path):
        os.startfile(path)


def parse_time_str(time_str: str) -> datetime.time:
    return datetime.datetime.strptime(time_str, '%H:%M').time()


def merge_dict(d: dict, u) -> dict:
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = merge_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d
