from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext

from notes_app.database import current_session, NoteRepo, Note, UserRepo, User
from notes_app.schemas import NotePydantic, UserPydantic

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@app.post("/create-user")
def create_user(user_data: UserPydantic):
    with current_session() as session:
        user_repo = UserRepo(session)
        user = user_repo.get_user(username=user_data.username)
        if user:
            raise HTTPException(status_code=409)
        hashed_password = get_password_hash(user_data.password)
        user = User(username=user_data.username, password=hashed_password)
        user_repo.add_user(user)
        session.commit()


@app.post("/create-note")
def create_note(head: str, body: str):
    with current_session() as session:
        note_repo = NoteRepo(session)
        note = Note(head=head, body=body)
        note_repo.add_note(note)
        session.commit()


@app.post("/delete-note")
def delete_note(note_id):
    with current_session() as session:
        note_repo = NoteRepo(session)
        note_repo.delete_note(note_id=note_id)
        session.commit()


@app.get("/read-note")
def read_note(note_id: int):
    with current_session() as session:
        note_repo = NoteRepo(session)
        note = note_repo.get_note(note_id=note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Заметка не найдена")
        else:
            note = NotePydantic(id=note.id, head=note.head,
                                body=note.body).model_dump()
            return note


@app.get("/list-notes")
def list_notes():
    with current_session() as session:
        note_repo = NoteRepo(session)
        notes = note_repo.get_notes()
        if not notes:
            raise HTTPException(status_code=404, detail="Заметки не найдены")
        else:
            pydantic_notes = [
                NotePydantic(id=n.id, head=n.head, body=n.body).model_dump()
                for n in notes]
            return pydantic_notes


if __name__ == "__main__":
    app()
