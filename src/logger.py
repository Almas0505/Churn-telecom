"""
Logging configuration module
Provides structured logging for the project
"""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up logger with console and optional file output
    
    Args:
        name: Logger name (typically __name__)
        log_file: Path to log file. If None, only logs to console
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Default format
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance with default configuration
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return setup_logger(name, log_file='logs/churn_prediction.log')


class LoggerMixin:
    """Mixin class to add logging capability to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return get_logger(name)


if __name__ == "__main__":
    # Example usage
    logger = get_logger(__name__)
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Example with LoggerMixin
    class DataProcessor(LoggerMixin):
        def process(self):
            self.logger.info("Processing data...")
            self.logger.info("Data processing complete")
    
    processor = DataProcessor()
    processor.process()
