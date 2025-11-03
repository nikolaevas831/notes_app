from notes_app.application.dto.note import NoteDTO
from notes_app.application.dto.user import UserDTO
from notes_app.application.exception import CurrentUserIdError, NoteNotFoundError
from notes_app.application.interfaces.note_repo import NoteRepoInterface, SyncNoteRepoInterface
from notes_app.application.interfaces.notifier import NotifierInterface
from notes_app.application.interfaces.txmanager import TxManagerInterface
from notes_app.application.mappers.note import NoteMapper
from notes_app.domain.entities.note import Note as NoteEntity


async def create_note(
    head: str,
    body: str,
    note_repo: NoteRepoInterface,
    current_user: UserDTO,
    tx_manager: TxManagerInterface,
    notifier: NotifierInterface,
) -> NoteDTO:
    note_entity = NoteEntity(head=head, body=body, user_id=current_user.id)
    saved_note = await note_repo.add_note(note_entity)
    await tx_manager.commit()
    await notifier.notify_note_created(note=saved_note)
    return NoteMapper.map_note_entity_to_dto(saved_note)


async def delete_note(
    note_id: int,
    note_repo: NoteRepoInterface,
    current_user: UserDTO,
    tx_manager: TxManagerInterface,
    notifier: NotifierInterface,
) -> None:
    note = await note_repo.get_note(note_id)
    if note is None:
        raise NoteNotFoundError
    if note.user_id != current_user.id:
        raise CurrentUserIdError
    await note_repo.delete_note(note_id)
    await tx_manager.commit()
    await notifier.notify_note_deleted(note=note)


async def read_note(
    note_id: int,
    note_repo: NoteRepoInterface,
    current_user: UserDTO,
) -> NoteDTO:
    note = await note_repo.get_note(note_id=note_id)
    if not note:
        raise NoteNotFoundError
    if note.user_id != current_user.id:
        raise CurrentUserIdError
    return NoteMapper.map_note_entity_to_dto(note)


async def get_list_notes(
    note_repo: NoteRepoInterface,
    current_user: UserDTO,
) -> list[NoteDTO]:
    notes = await note_repo.get_notes(user_id=current_user.id)
    return [NoteMapper.map_note_entity_to_dto(note) for note in notes]


def delete_all_notes(note_repo: SyncNoteRepoInterface) -> None:
    note_repo.delete_all_notes()
