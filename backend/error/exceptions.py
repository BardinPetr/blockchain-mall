class AuthenticationFailed(Exception):
    def __init__(self):
        super().__init__("Authentication failed")


class AuthenticationRequired(Exception):
    def __init__(self):
        super().__init__("Authentication required")


class UserIsNotLord(Exception):
    def __init__(self):
        super().__init__("This method is available only for the landlord")


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class RoomNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)