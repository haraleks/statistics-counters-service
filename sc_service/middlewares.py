from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from sc_service.settings import app_config


class CheckSecureTokenMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        secure_token = request.headers.get("SECURE-TOKEN")
        if (
                secure_token != app_config.secure_token and
                not request.url.path in ["/swagger/", "/swagger/apispec.json"]
        ):
            print(">>> Not Secure-Token<<<")
            return JSONResponse(status_code=401, content={})
        response = await call_next(request)
        return response
