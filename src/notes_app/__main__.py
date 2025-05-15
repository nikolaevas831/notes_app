import os
from datetime import timedelta, timezone, datetime
from typing import Annotated

import jwt
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from notes_app.database import current_session, NoteRepo, Note, UserRepo, User
from notes_app.schemas import NotePydantic, UserPydantic

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()


def get_session():
    with current_session() as session:
        yield session


def get_note_repo(session: Annotated[Session, Depends(get_session)]):
    note_repo = NoteRepo(session=session)
    return note_repo


def get_user_repo(session: Annotated[Session, Depends(get_session)]):
    user_repo = UserRepo(session=session)
    return user_repo


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(form_data_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(form_data_password, hashed_password)


def create_access_token(user_data: dict, expires_delta: timedelta):
    copied_user_data = user_data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    copied_user_data.update({"exp": expire})
    encoded_jwt = jwt.encode(copied_user_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     user_repo: Annotated[
                         UserRepo, Depends(get_user_repo)], ) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except InvalidTokenError:
        raise HTTPException(status_code=401)
    user = user_repo.get_user(username=username)
    if user is None:
        raise HTTPException(status_code=401)
    return user


@app.post("/create-user")
def create_user(user_data: UserPydantic,
                user_repo: Annotated[UserRepo, Depends(get_user_repo)]):
    username_check = user_repo.get_user(username=user_data.username)
    if username_check:
        raise HTTPException(status_code=409)
    hashed_password = get_password_hash(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    user_repo.add_user(user)
    user_repo.commit()


@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          user_repo: Annotated[UserRepo, Depends(get_user_repo)]):
    user = user_repo.get_user(username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Username not found")
    elif not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user_data={"sub": user.username},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/create-note")
def create_note(head: str, body: str,
                note_repo: Annotated[NoteRepo, Depends(get_note_repo)],
                current_user: Annotated[User, Depends(get_current_user)]):
    note = Note(head=head, body=body, user_id=current_user.id)
    note_repo.add_note(note)
    note_repo.commit()


@app.delete("/delete-note")
def delete_note(note_id: int,
                note_repo: Annotated[NoteRepo, Depends(get_note_repo)],
                current_user: Annotated[
                    User, Depends(get_current_user)], ) -> None:
    note = note_repo.get_note(note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403)
    note_repo.delete_note(note_id=note_id)
    note_repo.commit()


@app.get("/read-note")
def read_note(note_id: int,
              note_repo: Annotated[NoteRepo, Depends(get_note_repo)],
              current_user: Annotated[
                  User, Depends(get_current_user)], ) -> dict:
    note = note_repo.get_note(note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403)
    note = NotePydantic(id=note.id, head=note.head,
                        body=note.body,user_id=note.user_id).model_dump()
    return note


@app.get("/list-notes")
def list_notes(note_repo: Annotated[NoteRepo, Depends(get_note_repo)],
               current_user: Annotated[User, Depends(get_current_user)], ) -> \
        list[dict]:
    notes = note_repo.get_notes(user_id=current_user.id)
    if not notes:
        raise HTTPException(status_code=404, detail="Заметки не найдены")
    pydantic_notes = [
        NotePydantic(id=n.id, head=n.head, body=n.body,user_id=n.user_id).model_dump() for n in
        notes]
    return pydantic_notes

def main():
    uvicorn.run("notes_app.__main__:app",reload=True)

if __name__ == "__main__":
    main()
