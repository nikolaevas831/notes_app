import typer

from notes_app import database
from notes_app.database import current_session
from notes_app.schemas import Note as NotePydantic

app = typer.Typer()

@app.command()
def create_note(head: str, body: str):
    with current_session() as session:
        note = database.create_note(db=session, head=head, body=body)
        print(note)


@app.command()
def read_note(note_id: int):
    with current_session() as session:
        note = database.get_note(db=session, note_id=note_id)
        if not note:
            print("Заметка не найдена")
        else:
            validate_note = NotePydantic.model_validate(note)
            print(validate_note.model_dump())


@app.command()
def list_notes():
    with current_session() as session:
        notes = database.get_notes(db=session)
        for note in notes:
            validate_note = NotePydantic.model_validate(note)
            print(validate_note.model_dump())


if __name__ == "__main__":
    app()
