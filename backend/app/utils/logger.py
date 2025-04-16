import logging

logger = logging.getLogger("chatbot_logger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("chatbot.log")
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
