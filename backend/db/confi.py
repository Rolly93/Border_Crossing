import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    """configuracion base extraida de variables de entorno."""
    DEBUG =os.getenv('FLASK_DEBUG','False')=='True'
    SECRET_KEY = os.getenv('SECRET_KEY','default_secret_key')
    DATABASE_PATH = os.getenv('DATABASE_URL')
    PORT =int(os.getenv('PORT',5000))
    