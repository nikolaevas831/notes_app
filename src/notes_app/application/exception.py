class AuthError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass


class UsernameNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class NoteNotFoundError(Exception):
    pass


class CurrentUserIdError(Exception):
    pass
