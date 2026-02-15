import logging
import sys
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
        }
        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id
        
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = JSONFormatter()
    handler.setFormatter(formatter)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    logger.addHandler(handler)
    
    # Set levels for libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING) # Reduce noise
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return logger

logger = setup_logging()
