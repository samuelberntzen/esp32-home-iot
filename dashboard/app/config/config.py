import os 
from pydantic import BaseSettings, Field 

class Settings(BaseSettings):
    streamlit_user: str = Field(..., env='STREAMLIT_USER')
    streamlit_password: str = Field(..., env='STREAMLIT_PASSWORD')

    api_base_url: str = Field(..., env='API_BASE_URL') 

settings = Settings()


time_format = '%Y-%m-%dT%H:%M:%S'