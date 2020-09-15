import os
import multiprocessing as mp
from flask_env import MetaFlaskEnv


class Config(metaclass=MetaFlaskEnv):
    """Base configuration"""
    ENV_PREFIX = "LOGINSERVICE_"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    DEBUG = False
    SERVER_NAME = None
    # Logging
    LOG_FOLDER = "logs"
    FILE_LOGGING = True

    # Flask-Login: http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = os.environ.get(
        'FLASK_SECRET_KEY',
        'C6jP6YrXaDq8nchVyCF4DEuzwUSrPrRFAnAHH8A9Gutmy5vnTWyXdHWts4TnqeE3' * mp.cpu_count()
    )

    try:
        if not os.path.exists(LOG_FOLDER) or not os.access(LOG_FOLDER, os.W_OK):
            os.mkdir(LOG_FOLDER)
    except OSError as e:
        FILE_LOGGING = False

    LOG_NAME = 'info.log'
    LOG_PATH = os.path.join(LOG_FOLDER, LOG_NAME)
    LOG_MAX_BYTES = 0
    LOG_BACKUP_COUNT = 0

    # Backend
    API_URL = None


class ProdConfig(Config):
    """Production config"""
    #  Flask
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')


class TestConfig(Config):
    """Test configuration"""
    ENV = 'test'
    API_URL = 'http://localhost:5000/api/v2.0/'


class DevConfig(Config):
    """Development configuration"""
    ENV = 'dev'
    API_URL = 'http://localhost:5000/api/v2.0/'
