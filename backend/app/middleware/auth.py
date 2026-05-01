from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)

# Public routes that don't require authentication
PUBLIC_PATHS = {
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/auth/refresh",
}


class AuthLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log authenticated requests."""

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        method = request.method

        # Log request
        logger.debug(f"{method} {path}")

        response = await call_next(request)

        # Log response
        logger.debug(f"{method} {path} -> {response.status_code}")

        return response
