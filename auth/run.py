from datetime import timedelta
from typing import Annotated, List

from fastapi import Depends, HTTPException, status, FastAPI, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# from auth import crud
# from auth.db import get_db
from auth.dto.token import Token
from auth.dto.user import User, CreateUser
from auth.settings import settings
from auth.utils import authenticate_user, create_access_token, get_current_active_user
from auth.utils.user import fake_users_db, create_user_in_db, delete_user_in_db, get_current_user

app = FastAPI()


# выдает токен с инфой о пользователе другим сервисам - синхронная коммуникация (урок 4, 15:39)
# в другом сервисе инфа кладется в сессию и дальше берется оттуда
@app.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role,
            "id": str(user.external_id),
            "scopes": form_data.scopes
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/",
         response_model=User,
         dependencies=[Security(get_current_user, scopes=["me"])])
async def get_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


'''@app.get("/users/{user_id}/", response_model=User)
async def get_user_by_id(
        *, db: Annotated[Session, Depends(get_db)], user_id: int
):
    return crud.user.get(db=db, user_id=user_id)'''

'''
@app.get("/users/",
         response_model=List[User],
         dependencies=[Security(get_current_user, scopes=["list"])])
async def get_users(

):
    return [User(**user) for user in fake_users_db]


@app.post("/sign_up", response_model=User)
async def create_user(
    user_data: CreateUser
):
    # Event.send(User.Created, user_data)
    return create_user_in_db(fake_users_db, user_data)


@app.delete("/users/delete/{user_id}/", 
            response_model=str,
            dependencies=[Security(get_current_user, scopes=["delete"])])
async def delete_user(
    user_id: int
):
    delete_user_in_db(fake_users_db, user_id)
    return f"Пользователь с id={user_id} успешно удален из системы"
'''