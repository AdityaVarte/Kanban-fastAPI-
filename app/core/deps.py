from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Column, Card

from app.db.session import get_db
from app.core.jwt import decode_access_token
from app.models import User, Board

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = await db.get(User, int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return user


async def get_owned_board(
    board_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Board:
    board = await db.get(Board, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this board")
    return board

async def get_owned_column(
    column_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Column:
    column = await db.get(Column, column_id)
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")

    board = await db.get(Board, column.board_id)
    if board is None or board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this column")

    return column


async def get_owned_card(
    card_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Card:
    card = await db.get(Card, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    column = await db.get(Column, card.column_id)
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")

    board = await db.get(Board, column.board_id)
    if board is None or board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this card")

    return card

async def get_owned_column_by_id(
    column_id: int,
    db: AsyncSession,
    current_user: User,
) -> Column:
    column = await db.get(Column, column_id)
    if column is None:
        raise HTTPException(status_code=404, detail="Target column not found")
    board = await db.get(Board, column.board_id)
    if board is None or board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to use this column")
    return column