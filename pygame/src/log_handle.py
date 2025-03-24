import logging

def get_logger(name: str, level: int = logging.DEBUG):
    """
    Returns a preconfigured logger instance.
    
    Parameters:
        name (str): Name of the logger, typically __name__ of the module.
        level (int): Logging level. Defaults to DEBUG.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Check if logger already has handlers to avoid duplicate logs
    if not logger.hasHandlers():
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Define a standard format for all logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(console_handler)

    return logger
