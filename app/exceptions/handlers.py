"""
Exception handlers for FastAPI application
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback


class SEOAnalysisError(Exception):
    """Custom exception for SEO analysis errors"""
    def __init__(self, message: str, detail: str = None):
        self.message = message
        self.detail = detail
        super().__init__(message)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation error",
            "detail": errors
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )


async def seo_analysis_exception_handler(request: Request, exc: SEOAnalysisError):
    """Handle SEO analysis specific errors"""
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": exc.message,
            "detail": exc.detail
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if request.app.debug else "An unexpected error occurred"
        }
    )


def register_exception_handlers(app: FastAPI):
    """Register all exception handlers"""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(SEOAnalysisError, seo_analysis_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)