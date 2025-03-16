from typing import Literal

import pydantic_settings
from helpers.path import relative_from_root

BrowserType = Literal['chrome', 'firefox', 'edge']


class Config(pydantic_settings.BaseSettings):
    base_url: str = 'https://samokat.ru'
    login: str
    password: str
    browser_name: BrowserType = 'firefox'
    browser_version: str = '125.0'
    run_mode: str = 'local'
    window_width: int = 1920
    window_height: int = 1080


config = Config(_env_file=relative_from_root('.env'))
