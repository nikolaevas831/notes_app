import typer

from notes_app import database
from notes_app.database import current_session
from notes_app.schemas import Note as NotePydantic

app = typer.Typer()


def get_db_session():
    db = current_session()
    try:
        yield db
    finally:
        db.close()


@app.command()
def create_note(head: str, body: str):
    db = next(get_db_session())
    note = database.create_note(db=db, head=head, body=body)
    print(note)


@app.command()
def read_note(note_id: int):
    db = next(get_db_session())
    note = database.get_note(db=db, note_id=note_id)
    if not note:
        print("Заметка не найдена")
    else:
        validate_note = NotePydantic.model_validate(note)
        print(validate_note.model_dump())


@app.command()
def list_notes():
    db = next(get_db_session())
    notes = database.get_notes(db=db)
    for note in notes:
        validate_note = NotePydantic.model_validate(note)
        print(validate_note.model_dump())


if __name__ == "__main__":
    app()
