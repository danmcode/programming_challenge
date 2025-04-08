import logging
import sys
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Configura y devuelve un logger con handlers para console, info.log y error.log"""
    
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    file_handler_info = RotatingFileHandler(
        os.path.join(log_dir, 'info.log'), 
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    file_handler_error = RotatingFileHandler(
        os.path.join(log_dir, 'error.log'), 
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler_error.setLevel(logging.ERROR)
    file_handler_error.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    if root_logger.handlers:
        root_logger.handlers.clear()
        
    root_logger.addHandler(file_handler_info)
    root_logger.addHandler(file_handler_error)
    root_logger.addHandler(console_handler)
    
    return root_logger

logger = setup_logging()

def get_logger(name):
    """Devuelve un logger con el nombre especificado que usa la configuración global"""
    return logging.getLogger(name)