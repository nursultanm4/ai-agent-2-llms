import logging
import logging.handlers
import os
from datetime import datetime
from config import settings


def setup_logger():
    """Setup and configure the application logger"""
    
    # Create logs directory if it doesnt exist
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("ai_agent")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Clear up the existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # file handler with rotation
    log_file_path = os.path.join(settings.LOG_DIR, settings.LOG_FILE)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=settings.LOG_MAX_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create and export logger instance
logger = setup_logger()


def log_request(request_id: str, endpoint: str, method: str, user_query: str = None):
    """Log incoming request details"""
    logger.info(f"Request {request_id}: {method} {endpoint}")
    if user_query:
        logger.info(f"Request {request_id}: User query: {user_query[:100]}...")

def log_response(request_id: str, response_time: float, status_code: int, cached: bool = False):
    """Log response details"""
    logger.info(f"Request {request_id}: Response in {response_time:.2f}s, Status: {status_code}, Cached: {cached}")

def log_error(request_id: str, error: Exception, context: str = ""):
    """Log error details"""
    logger.error(f"Request {request_id}: Error in {context}: {str(error)}", exc_info=True)

def log_llm_call(request_id: str, model: str, prompt: str, response: str, duration: float):
    """Log LLM API call details"""
    logger.info(f"Request {request_id}: {model} call completed in {duration:.2f}s")
    logger.debug(f"Request {request_id}: {model} prompt: {prompt[:100]}...")
    logger.debug(f"Request {request_id}: {model} response: {response[:200]}...")