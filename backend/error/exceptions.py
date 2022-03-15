class AuthenticationFailed(Exception):
    def __init__(self):
        super().__init__("Authentication failed")
