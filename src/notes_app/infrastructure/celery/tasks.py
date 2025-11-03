
from notes_app.application.usecases.note import delete_all_notes
from notes_app.infrastructure.celery.celery_app import celery_app
from notes_app.infrastructure.database.main import sync_current_session
from notes_app.infrastructure.database.repositories.note import SyncNoteRepo


@celery_app.task
def delete_notes_task():
    with sync_current_session() as session:
        try:
            note_repo = SyncNoteRepo(session)
            delete_all_notes(note_repo)
            session.commit()
        except Exception:
            session.rollback()
            raise