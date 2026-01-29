from celery import shared_task
from dishka.integrations.celery import FromDishka, inject

from notes_app.application.usecases.note import delete_all_notes as delete_all_notes_usecase
from notes_app.infrastructure.database.repositories.note import SyncNoteRepo
from notes_app.infrastructure.database.tx_manager import SyncTxManagerImpl


@shared_task(name="delete_notes")
@inject
def delete_notes_task(
    tx_manager: FromDishka[SyncTxManagerImpl], note_repo: FromDishka[SyncNoteRepo]
) -> None:
    delete_all_notes_usecase(tx_manager=tx_manager, note_repo=note_repo)
