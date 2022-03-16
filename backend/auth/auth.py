from auth.signatures import decode_token


def get_access_token(info):
    cookies = info.context['request'].cookies
    print("IN get_access_token - cookies:", cookies)
    access_token = cookies.get('access_token_cookie')
    if access_token is None:
        access_token = info.context['request'].headers.get('CookiePlayground')
        if access_token is None:
            return None
        access_token = access_token.split("=")[1]
    return decode_token(access_token)
