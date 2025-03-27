import logging
import os
import sys
from datetime import datetime

def setup_logging():
    """
    Set up and configure the logger.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logger = logging.getLogger('streamlit_app')
    
    # Check if handler is already configured to avoid duplicate handlers
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create file handler
        log_file = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

def log_message(logger, level, message):
    """
    Log a message with the specified level.
    
    Args:
        logger (logging.Logger): Logger instance
        level (str): Log level ('debug', 'info', 'warning', 'error', 'critical')
        message (str): Message to log
    """
    if level == 'debug':
        logger.debug(message)
    elif level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    elif level == 'critical':
        logger.critical(message)
    else:
        logger.info(message)
