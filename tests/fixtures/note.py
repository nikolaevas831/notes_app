from typing import TypedDict

import pytest
from faker import Faker


class NoteCreateDict(TypedDict):
    head: str
    body: str


@pytest.fixture
def note_create_schema(faker: Faker) -> NoteCreateDict:
    return {"head": faker.text(), "body": faker.text()}
