from celery import shared_task
from dishka.integrations.celery import FromDishka, inject
from sqlalchemy.orm.session import Session

from notes_app.application.usecases.note import delete_all_notes as delete_all_notes_usecase
from notes_app.infrastructure.database.repositories.note import SyncNoteRepo


@shared_task(name="delete_notes")
@inject
def delete_notes_task(db_session: FromDishka[Session], note_repo: FromDishka[SyncNoteRepo]) -> None:
    with db_session as session:
        try:
            delete_all_notes_usecase(note_repo)
            session.commit()

        except Exception:
            session.rollback()
            raise
