from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import books

app = FastAPI(title="Library API – Khoa CNTT", version="1.0.0",
              description="API quản lý sách của Thư viện số Khoa CNTT")

ERROR_NAMES = {400: "bad_request", 404: "not_found",
               409: "conflict", 422: "validation_error"}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": ERROR_NAMES.get(exc.status_code, "error"),
                 "message": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = "; ".join(
        f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in exc.errors()
    )
    return JSONResponse(status_code=422,
                        content={"error": "validation_error", "message": message})


app.include_router(books.router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
