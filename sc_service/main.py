from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi_pagination import add_pagination
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from sc_service.api.all_routers import router
from sc_service.exceptions.base import parsing_pydentic_errors
from sc_service.middlewares import CheckSecureTokenMiddleware


def init_routers(app: FastAPI) -> None:
    app.include_router(router)


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(CheckSecureTokenMiddleware)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Statics counter service docs (version: 1)",
        version="v1",
        docs_url="/swagger/",
        openapi_url="/swagger/apispec.json",
        description="## REST API",
    )
    init_routers(app)
    add_pagination(app)
    init_middlewares(app)

    return app


app: FastAPI = create_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    reformatted_message = parsing_pydentic_errors(exc)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"error": HTTPStatus.BAD_REQUEST.description, "detail": reformatted_message}
        ),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"error": exc.error, "detail": exc.detail}),
    )
