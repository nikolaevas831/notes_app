from dishka.integrations.celery import FromDishka, inject
from sqlalchemy.orm.session import Session

from notes_app.application.usecases.note import delete_all_notes
from notes_app.infrastructure.database.repositories.note import SyncNoteRepo
from notes_app.infrastructure.task_scheduler.main import celery_app


@celery_app.task
@inject
def delete_notes_task(db_session: FromDishka[Session], note_repo: FromDishka[SyncNoteRepo]) -> None:
    with db_session as session:
        try:
            delete_all_notes(note_repo)
            session.commit()

        except Exception:
            session.rollback()
            raise
