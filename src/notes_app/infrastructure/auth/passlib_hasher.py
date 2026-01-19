from passlib.context import CryptContext

from notes_app.application.interfaces.hasher import HasherInterface


class PasslibHasherImpl(HasherInterface):
    def __init__(self) -> None:
        self.password_context = CryptContext(
            schemes=["bcrypt"],
            bcrypt__rounds=8,
            bcrypt__ident="2b",
            deprecated="auto",
        )

    def hash_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(self, form_data_password: str, hashed_password: str) -> bool:
        return self.password_context.verify(form_data_password, hashed_password)
