from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from bson.errors import InvalidId

from app.error_handler import (
    validation_exception_handler,
    type_error_handler,
    invalid_company_id_handler,
    company_not_found_error_handler,
    default_error_handler,
)

from app.routes import router as company_router

app = FastAPI()

# Add custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(TypeError, type_error_handler)
app.add_exception_handler(InvalidId, invalid_company_id_handler)
app.add_exception_handler(HTTPException, company_not_found_error_handler)
app.add_exception_handler(Exception, default_error_handler)

# add routes
app.include_router(company_router, prefix="/companies", tags=["Companies"])