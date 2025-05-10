import typer

from notes_app import database
from notes_app.database import current_session
from notes_app.schemas import Note as NotePydantic

app = typer.Typer()


@app.command()
def create_note(head: str, body: str):
    with current_session() as session:
        note_repo = NoteRepo(session)
        note = Note(head=head, body=body)
        note_repo.add_note(note)
        session.commit()
        print(note)


@app.command()
def read_note(note_id: int):
    with current_session() as session:
        note_repo = NoteRepo(session)
        note = note_repo.get_note(note_id=note_id)
        if not note:
            print("Заметка не найдена")
        else:
            note = NotePydantic(id=note.id, head=note.head,
                                body=note.body).model_dump()
            print(note)


@app.command()
def list_notes():
    with current_session() as session:
        note_repo = NoteRepo(session)
        notes = note_repo.get_notes()
        print(notes)
        for note in notes:
            note = NotePydantic(id=note.id, head=note.head,
                                body=note.body).model_dump()
            print(note)


if __name__ == "__main__":
    app()
