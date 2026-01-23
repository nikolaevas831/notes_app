from notes_app.application.interfaces.hasher import HasherInterface


class HasherMock(HasherInterface):
    def __init__(self) -> None:
        self.password_context: str = "_hashed"  # noqa: S105

    def hash_password(self, password: str) -> str:
        return f"{password}+{self.password_context}"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        expected_hash = f"{plain_password}+{self.password_context}"
        return expected_hash == hashed_password
