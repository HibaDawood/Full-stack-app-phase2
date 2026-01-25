import logging
from datetime import datetime
from typing import Optional
from ..models.user import User
from ..models.task import Task


def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )


def log_task_operation(operation: str, user: User, task: Optional[Task] = None, details: str = ""):
    """Log task operations for audit trail"""
    logger = logging.getLogger(__name__)
    task_info = f"Task ID: {task.id}" if task else "No Task"
    logger.info(f"User {user.id} ({user.email}) performed {operation} - {task_info}. Details: {details}")


def log_authentication_attempt(user_email: str, success: bool, details: str = ""):
    """Log authentication attempts"""
    logger = logging.getLogger(__name__)
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Authentication attempt for {user_email}: {status}. Details: {details}")