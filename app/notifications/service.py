import logging

logger = logging.getLogger("notifications")

def send_notification(user_id: int, message: str):
    # Synchronous logging-based notifications only
    logger.info(f"NOTIFICATION to User {user_id}: {message}")
