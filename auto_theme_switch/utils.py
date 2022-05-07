import ctypes
import subprocess


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


def set_registry_value(key: str, value: str, data: str):
    command = ['reg.exe', 'add', key, '/v', value, '/t', 'REG_DWORD', '/d', data, '/f']
    subprocess.run(command, stdout=subprocess.DEVNULL)
