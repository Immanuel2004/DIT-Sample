import logging
import os

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file path
LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

# Configure logger
logger = logging.getLogger("dynamic-impact-tool")
logger.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s — %(levelname)s — %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers only once to avoid duplication on reruns
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
