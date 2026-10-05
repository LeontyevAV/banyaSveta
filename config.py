from pathlib import Path

import yaml
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).resolve().parent
YAML_PATH = BASE_DIR / 'settings.yaml'


class YamlSettingsSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        self._data: dict = {}
        if YAML_PATH.exists():
            raw = yaml.safe_load(YAML_PATH.read_text(encoding='utf-8')) or {}
            if isinstance(raw, dict):
                self._data = raw

    def get_field_value(self, field, field_name: str) -> tuple:
        return self._data.get(field_name), field_name, False

    def __call__(self) -> dict:
        fields = self.settings_cls.model_fields
        return {k: v for k, v in self._data.items() if k in fields}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False,
    )

    bot_name: str = '@banya_sveta_bot'
    bot_token: str = ''
    system_token: str = ''
    channel_info: str = ''
    proxy_url: str = ''
    debug: bool = False
    debug_user_id: int | None = None

    pg_host: str = 'localhost'
    pg_port: int = 5432
    pg_database: str = 'labots'
    pg_username: str = 'postgres'
    pg_password: str = ''

    log_level: str = 'WARNING'

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlSettingsSource(settings_cls),
            file_secret_settings,
        )


settings = Settings()
