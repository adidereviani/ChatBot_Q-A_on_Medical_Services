import logging
import os

# Create a logger for the chatbot
logger = logging.getLogger("chatbot_logger")
logger.setLevel(logging.INFO)

# Set up logging to a file
log_file = os.path.join(os.path.dirname(__file__), "chatbot.log")
handler = logging.FileHandler(log_file, encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
