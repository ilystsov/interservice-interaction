from pydantic import BaseSettings


class AppSetting(BaseSettings):
    log_level: str = 'DEBUG'
    db: str = ''

    class Config:
        env_prefix = 'APP_'


app_settings = AppSetting()
