# Carga y valida las variables de entorno usando Pydantic Settings.
# Si falta una variable obligatoria, la app falla al arrancar (mejor que fallar en runtime).
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str          # cadena de conexion a MySQL
    frontend_origin: str       # origen permitido para CORS

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()