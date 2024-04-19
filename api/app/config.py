from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    model_name: str = None
    vectorizer_name: str = None
    threshold: float = None

@lru_cache
def get_settings():   #HEREDA LO QUE TIENE LA CLASE PADRE. LEE LOS AJUSTES DESDE DONDE SE ESPECIFIQUE
    return Settings(_env_file="app/settings.env")
