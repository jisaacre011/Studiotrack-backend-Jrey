# Carga y valida las variables de entorno usando Pydantic Settings.
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str          # cadena de conexion a MySQL
    frontend_origin: str       # origen permitido para CORS
    admin_key: str             # clave de administrador para operaciones protegidas

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
