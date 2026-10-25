from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.core.deps import get_current_user, get_owned_board
from app.models import Board, Column, User
from app.schemas.board import BoardCreate, BoardRead, BoardWithColumns

router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/", response_model=BoardRead, status_code=201)
async def create_board(
    board_in: BoardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_board = Board(name=board_in.name, owner_id=current_user.id)
    db.add(new_board)
    await db.commit()
    await db.refresh(new_board)
    return new_board


@router.get("/", response_model=list[BoardRead])
async def list_boards(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Board).where(Board.owner_id == current_user.id))
    return result.scalars().all()


@router.get("/{board_id}", response_model=BoardWithColumns)
async def get_board(
    board: Board = Depends(get_owned_board),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Board)
        .where(Board.id == board.id)
        .options(selectinload(Board.columns).selectinload(Column.cards))
    )
    return result.scalar_one()


@router.put("/{board_id}", response_model=BoardRead)
async def update_board(
    board_in: BoardCreate,
    board: Board = Depends(get_owned_board),
    db: AsyncSession = Depends(get_db),
):
    board.name = board_in.name
    await db.commit()
    await db.refresh(board)
    return board


@router.delete("/{board_id}", status_code=204)
async def delete_board(
    board: Board = Depends(get_owned_board),
    db: AsyncSession = Depends(get_db),
):
    await db.delete(board)
    await db.commit()