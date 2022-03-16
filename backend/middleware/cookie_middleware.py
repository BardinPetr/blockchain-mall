from starlette.middleware.base import BaseHTTPMiddleware


class CookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        request = await request.json()
        response.headers['Custom'] = 'Example'
        return response
