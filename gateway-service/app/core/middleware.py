from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.utils.exceptions import AppError
import logging
import traceback
import uuid

logger = logging.getLogger("api.error")

async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    if isinstance(exc, AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "detail": exc.message,
                "request_id": request_id,
                "context": exc.details
            }
        )
    
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "ValidationError",
                "detail": "Input validation failed",
                "request_id": request_id,
                "context": {"errors": exc.errors()}
            }
        )
        
    if isinstance(exc, SQLAlchemyError):
        logger.error(f"Database Error: {str(exc)}", extra={"request_id": request_id})
        # Mask internal DB errors
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "DatabaseError",
                "detail": "An internal database error occurred.",
                "request_id": request_id
            }
        )

    # General fallback
    logger.error(f"Unhandled Exception: {str(exc)}\n{traceback.format_exc()}", extra={"request_id": request_id})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "detail": "An unexpected error occurred.",
            "request_id": request_id
        }
    )
