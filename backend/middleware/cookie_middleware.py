from starlette.middleware.base import BaseHTTPMiddleware


class CookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Set-Cookie'] = 'access_token_cookie=bipki'
        response.headers['Cookie'] = 'access_token_cookie=bipki'
        print("IN CookieMiddleware - response headers:", response.headers)
        return response