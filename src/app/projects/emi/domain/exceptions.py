class EmailAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass

class EmptyOrderError(Exception):
    pass


class StockInsuficienteError(Exception):
    pass