"""Init file for utils package."""
from .logger import Logger
from .constants import (
    PROJECT_NAME,
    DEFAULT_LOG_LEVEL,
    CONFIG_FILE_NAME,
    API_PREFIX,
    API_TITLE,
    API_VERSION,
    API_DOCS_URL,
    INTERNAL_SERVER_ERROR_STRING,
    BACKEND_FILE_PATH,
    MIN_AGE_LIMIT,
    POLL_INTERVAL,
    DUMMY_EMAIL,
    DUMMY_PASSWORD,
)
from .send_email import send_email
