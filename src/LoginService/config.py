import os


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
