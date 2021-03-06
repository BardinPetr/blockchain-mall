class AuthenticationFailed(Exception):
    def __init__(self):
        super().__init__("Authentication failed")


class AuthenticationRequired(Exception):
    def __init__(self):
        super().__init__("Authentication required")


class UserIsNotLord(Exception):
    def __init__(self):
        super().__init__("This method is available only for the landlord")


class UserIsNotCashier(Exception):
    def __init__(self):
        super().__init__("This method is available only for the cashiers")


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class RoomNotExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class TicketNotExistsError(Exception):
    def __init__(self):
        super().__init__("Ticket with such ID not found")


class ContractNotExistsError(Exception):
    def __init__(self):
        super().__init__("Contract with such address not found")

