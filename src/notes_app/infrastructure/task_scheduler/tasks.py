from sqlalchemy.orm.session import Session, sessionmaker

from notes_app.application.usecases.note import delete_all_notes
from notes_app.infrastructure.database.repositories.note import SyncNoteRepo
from notes_app.infrastructure.task_scheduler.main import celery_app, db_session_factory


def get_db_session(session_factory: sessionmaker[Session] = db_session_factory) -> Session:
    return session_factory()


def get_note_repo(session: Session | None) -> SyncNoteRepo:
    if session is None:
        session = get_db_session()
    return SyncNoteRepo(session)


@celery_app.task
def delete_notes_task() -> None:
    db_session: Session = get_db_session(session_factory=db_session_factory)
    with db_session as session:
        note_repo: SyncNoteRepo = get_note_repo(session=session)
        try:
            delete_all_notes(note_repo)
            session.commit()

        except Exception:
            session.rollback()
            raise
