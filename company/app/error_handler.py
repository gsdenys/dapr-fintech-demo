from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from bson.errors import InvalidId
from fastapi import HTTPException


# @app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Custom handler for validation errors.
    Args:
        request: The incoming request.
        exc: The validation exception raised.
    Returns:
        JSONResponse: A formatted error response with a human-readable message.
    """
    errors = exc.errors()
    formatted_errors = [
        {
            "field": err.get("loc", ["unknown"])[-1],
            "message": err.get("msg", "Invalid input"),
        }
        for err in errors
    ]
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "errors": formatted_errors},
    )


# @app.exception_handler(TypeError)
async def type_error_handler(request, exc: TypeError):
    """
    Custom handler for InvalidId.
    """
    return JSONResponse(
        status_code=400,
        content={"message": "The provided company ID is invalid."},
    )


# @app.exception_handler(InvalidId)
async def invalid_company_id_handler(request, exc: InvalidId):
    """
    Custom handler for InvalidId.
    """
    return JSONResponse(
        status_code=400,
        content={"message": "The provided company ID is invalid."},
    )


# @app.exception_handler(HTTPException)
async def company_not_found_error_handler(request, exc: HTTPException):
    """
    Custom handler for InvalidId.
    """
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "Company not found"},
        )

    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )


# @app.exception_handler(Exception)
async def default_error_handler(request, exc: Exception):
    """
    Custom handler for InvalidId.
    """
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )
