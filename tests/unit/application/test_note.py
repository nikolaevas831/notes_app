from unittest.mock import AsyncMock

import pytest

from notes_app.application.dto.note import CreateNoteDTO
from notes_app.application.dto.user import UserDTO
from notes_app.application.usecases.note import create_note
from tests.mocks.note_repo import NoteRepoMock
from tests.mocks.tx_manager import TxManagerMock

pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


async def test_create_user(
    note_create_dto: CreateNoteDTO,
    note_repo_mock: NoteRepoMock,
    current_user_dto: UserDTO,
    tx_manager_mock: TxManagerMock,
    notifier_mock: AsyncMock,
) -> None:
    result = await create_note(
        note_data=note_create_dto,
        note_repo=note_repo_mock,
        current_user=current_user_dto,
        tx_manager=tx_manager_mock,
        notifier=notifier_mock,
    )

    assert result.head == note_create_dto.head
    assert result.user_id == note_create_dto.user_id
    assert result.id is not None
    saved_note = await note_repo_mock.get_note(note_id=result.id)
    assert saved_note is not None
    assert saved_note.head == note_create_dto.head
    assert saved_note.user_id == note_create_dto.user_id
    assert saved_note.body == note_create_dto.body
