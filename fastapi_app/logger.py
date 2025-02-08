import logging
import os

def _parse_log_level(level_str: str | None) -> int:
    """Convert string log level to logging constant."""
    if not level_str:
        return logging.INFO
        
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    return level_map.get(level_str.upper(), logging.INFO)

def setup_logger(name: str, level: int | None = None) -> logging.Logger:
    """
    Configure and return a logger instance with console output.
    
    Args:
        name: The name of the logger (typically __name__ from the calling module)
        level: The logging level (default: None, will use LOG_LEVEL env var or INFO)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Get log level from environment variable or use provided level or default to INFO
    log_level = level or _parse_log_level(os.getenv('LOG_LEVEL'))
    
    logger = logging.getLogger(name)
    
    # Prevent adding handlers multiple times if logger already exists
    if not logger.handlers:
        logger.setLevel(log_level)
        
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger