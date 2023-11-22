from pydantic import BaseSettings


class AppSetting(BaseSettings):
    black_list_host: str = 'http://blacklist_tests:8001'
    log_level: str = 'DEBUG'
    db: str = ''

    class Config:
        env_prefix = 'APP_'


app_settings = AppSetting()
