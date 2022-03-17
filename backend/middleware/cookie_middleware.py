from starlette.middleware.base import BaseHTTPMiddleware

from auth.signatures import get_last_token, clear_last_token


class CookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # cookie = "access_token_cookie=bipki"
        if get_last_token() is not None:
            cookie = "access_token_cookie=" + get_last_token()
            response.headers['Set-Cookie'] = cookie
            response.headers['Cookie'] = cookie
            clear_last_token()
        print("IN CookieMiddleware - response headers:", response.headers)
        return response
