import pytest
from faker import Faker

from notes_app.api.models.note import NoteCreateSchema
from notes_app.application.dto.note import CreateNoteDTO
from notes_app.application.dto.user import UserDTO


@pytest.fixture
def note_create_schema(faker: Faker) -> NoteCreateSchema:
    return NoteCreateSchema(head=faker.text(), body=faker.text())


@pytest.fixture
def note_create_dto(faker: Faker, current_user_dto: UserDTO) -> CreateNoteDTO:
    return CreateNoteDTO(head=faker.text(), body=faker.text(), user_id=current_user_dto.id)
