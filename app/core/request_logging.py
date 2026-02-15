import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.time()
        
        # Log Request
        logger.info(f"Request started: {request.method} {request.url.path}", extra={"request_id": request_id})
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log Response
            logger.info(
                f"Request completed: {response.status_code} in {process_time:.4f}s",
                extra={"request_id": request_id}
            )
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {str(e)} in {process_time:.4f}s",
                extra={"request_id": request_id}
            )
            raise e
