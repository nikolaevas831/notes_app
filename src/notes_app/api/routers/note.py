from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from notes_app.api.models.note import NoteCreateSchema, NoteResponseSchema
from notes_app.api.providers import (
    get_current_user,
    get_note_repo,
    get_notifier,
    get_tx_manager,
)
from notes_app.application.dto.note import CreateNoteDTO, NoteDTO
from notes_app.application.dto.user import UserDTO
from notes_app.application.exception import CurrentUserIdError, NoteNotFoundError
from notes_app.application.interfaces.note_repo import NoteRepoInterface
from notes_app.application.interfaces.notifier import NotifierInterface
from notes_app.application.interfaces.txmanager import TxManagerInterface
from notes_app.application.usecases.note import (
    create_note as application_create_note,
    delete_note as application_delete_note,
    get_list_notes as application_get_list_notes,
    read_note as application_read_note,
)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreateSchema,
    note_repo: Annotated[NoteRepoInterface, Depends(get_note_repo)],
    current_user: Annotated[UserDTO, Depends(get_current_user)],
    tx_manager: Annotated[TxManagerInterface, Depends(get_tx_manager)],
    notifier: Annotated[NotifierInterface, Depends(get_notifier)],
) -> NoteResponseSchema:
    note_dto = CreateNoteDTO(head=note_data.head, body=note_data.body, user_id=current_user.id)
    note = await application_create_note(
        note_data=note_dto,
        note_repo=note_repo,
        current_user=current_user,
        tx_manager=tx_manager,
        notifier=notifier,
    )
    return NoteResponseSchema(id=note.id, user_id=note.user_id, head=note.head, body=note.body)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    note_repo: Annotated[NoteRepoInterface, Depends(get_note_repo)],
    current_user: Annotated[UserDTO, Depends(get_current_user)],
    tx_manager: Annotated[TxManagerInterface, Depends(get_tx_manager)],
    notifier: Annotated[NotifierInterface, Depends(get_notifier)],
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


@router.get("/{note_id}")
async def get_note_by_id(
    note_id: int,
    note_repo: Annotated[NoteRepoInterface, Depends(get_note_repo)],
    current_user: Annotated[UserDTO, Depends(get_current_user)],
) -> NoteResponseSchema:
    try:
        note = await application_read_note(
            note_id=note_id,
            note_repo=note_repo,
            current_user=current_user,
        )

    except NoteNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Note not found") from err
    except CurrentUserIdError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from err
    else:
        return NoteResponseSchema(id=note.id, user_id=note.user_id, head=note.head, body=note.body)


@router.get("/")
async def get_notes(
    note_repo: Annotated[NoteRepoInterface, Depends(get_note_repo)],
    current_user: Annotated[UserDTO, Depends(get_current_user)],
) -> list[NoteResponseSchema]:
    notes: list[NoteDTO] = await application_get_list_notes(
        note_repo=note_repo, current_user=current_user
    )
    return [
        NoteResponseSchema(id=note.id, user_id=note.user_id, head=note.head, body=note.body)
        for note in notes
    ]
