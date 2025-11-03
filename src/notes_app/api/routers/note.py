
from fastapi import APIRouter, Depends, HTTPException

from notes_app.api.models.note import NoteCreateSchema, NoteResponseSchema
from notes_app.api.providers import (
    get_current_user,
    get_note_created_notifier,
    get_note_deleted_notifier,
    get_note_repo,
    get_tx_manager,
)
from notes_app.application.exception import CurrentUserIdError, NoteNotFoundError
from notes_app.application.interfaces.note_repo import NoteRepoInterface
from notes_app.application.interfaces.notifier import NotifierInterface
from notes_app.application.interfaces.txmanager import TxManagerInterface
from notes_app.application.usecases.note import (
    create_note as application_create_note,
)
from notes_app.application.usecases.note import (
    delete_note as application_delete_note,
)
from notes_app.application.usecases.note import (
    get_list_notes as application_get_list_notes,
)
from notes_app.application.usecases.note import (
    read_note as application_read_note,
)
from notes_app.domain.entities.user import User

router = APIRouter(prefix="/notes")


@router.post("/", status_code=201, response_model=NoteResponseSchema)
async def create_note(
    note_data: NoteCreateSchema,
    note_repo: NoteRepoInterface = Depends(get_note_repo),
    current_user: User = Depends(get_current_user),
    tx_manager: TxManagerInterface = Depends(get_tx_manager),
    notifier: NotifierInterface = Depends(get_note_created_notifier),
) -> NoteResponseSchema:
    note = await application_create_note(
        head=note_data.head,
        body=note_data.body,
        note_repo=note_repo,
        current_user=current_user,
        tx_manager=tx_manager,
        notifier=notifier,
    )
    return note


@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: int,
    note_repo: NoteRepoInterface = Depends(get_note_repo),
    current_user: User = Depends(get_current_user),
    tx_manager: TxManagerInterface = Depends(get_tx_manager),
    notifier: NotifierInterface = Depends(get_note_deleted_notifier),
) -> None:
    try:
        await application_delete_note(
            note_id=note_id,
            note_repo=note_repo,
            current_user=current_user,
            tx_manager=tx_manager,
            notifier=notifier,
        )
    except NoteNotFoundError as err:
        raise HTTPException(status_code=404, detail="Note not found") from err
    except CurrentUserIdError as err:
        raise HTTPException(status_code=404) from err


@router.get("/{note_id}", response_model=NoteResponseSchema)
async def get_note_by_id(
    note_id: int,
    note_repo: NoteRepoInterface = Depends(get_note_repo),
    current_user: User = Depends(get_current_user),
) -> NoteResponseSchema:
    try:
        note = await application_read_note(
            note_id=note_id,
            note_repo=note_repo,
            current_user=current_user,
        )
        return note
    except NoteNotFoundError as err:
        raise HTTPException(status_code=404, detail="Note not found") from err
    except CurrentUserIdError as err:
        raise HTTPException(status_code=403) from err


@router.get("/", response_model=list[NoteResponseSchema])
async def get_notes(
    note_repo: NoteRepoInterface = Depends(get_note_repo),
    current_user: User = Depends(get_current_user),
) -> list[NoteResponseSchema]:
    return await application_get_list_notes(note_repo=note_repo, current_user=current_user)
