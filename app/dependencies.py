from typing import Annotated

from fastapi import Header, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_jwt(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
