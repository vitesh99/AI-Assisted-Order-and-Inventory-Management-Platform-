from typing import Any, Dict, Optional

class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class NotFoundException(AppError):
    def __init__(self, detail: str):
        super().__init__(message=detail, status_code=404)

class StockException(AppError):
    def __init__(self, detail: str):
        super().__init__(message=detail, status_code=400)

class AuthError(AppError):
    def __init__(self, detail: str):
        super().__init__(message=detail, status_code=401)
