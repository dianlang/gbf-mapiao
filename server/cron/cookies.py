import os
import json
import pathlib
import config
from typing import List, Dict
from vars import cron_dir


def loadCookies():
    with open(str(cron_dir / 'cookie.json'), 'r', encoding='utf8') as f:
        cookies = json.load(f)  # type: Dict[str,str]
    return cookies


def get_chrome_cookies(url, profile: str = 'Default'):
    import os
    import sqlite3
    import win32crypt

    cookie_file_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\{}\Cookies'.format(profile))
    conn = sqlite3.connect(cookie_file_path)
    ret_dict = {}
    rows = list(conn.execute("select name, encrypted_value from cookies where host_key = '{}'".format(url)))
    conn.close()
    for row in rows:
        ret = win32crypt.CryptUnprotectData(row[1], None, None, None, 0)
        ret_dict[row[0]] = ret[1].decode()
    return ret_dict


try:
    cookies = loadCookies()
except FileNotFoundError:
    try:
        # if 1:
        cookies = get_chrome_cookies('game.granbluefantasy.jp', profile=config.profile)
        with open(str(cron_dir / 'cookie.json'), 'w+', encoding='utf8') as f:
            json.dump(cookies, f)  # type: Dict[str, str]
    except ImportError:
        raise Exception('no cookies given')
