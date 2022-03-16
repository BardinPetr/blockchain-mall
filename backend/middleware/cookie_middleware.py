from starlette.middleware.base import BaseHTTPMiddleware


class CookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Cookie'] = 'access_token_cookie=bipki'
        return response
