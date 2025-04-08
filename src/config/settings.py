import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_BASE_URL= os.getenv("API_BASE_URL")
    API_KEY = os.getenv("API_KEY")

    TEST_ENDPOINT= os.getenv("TEST_ENDPOINT")
    AI_ENDPOINT= os.getenv("AI_ENDPOINT")
    PROD_ENDPOINT= os.getenv("PROD_ENDPOINT")
    SOLUTION_ENDPOINT= os.getenv("SOLUTION_ENDPOINT")

    POKE_API= os.getenv("POKE_API")
    SWAPI= os.getenv("SWAPI")
    
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
settings = Settings()