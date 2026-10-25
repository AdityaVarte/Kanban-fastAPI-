from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.deps import get_current_user, get_owned_column
from app.models import Column, Board, User
from app.schemas.column import ColumnCreate, ColumnRead

router = APIRouter(prefix="/columns", tags=["columns"])


@router.post("/", response_model=ColumnRead, status_code=201)
async def create_column(
    column_in: ColumnCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    board = await db.get(Board, column_in.board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add columns to this board")

    new_column = Column(
        name=column_in.name,
        position=column_in.position,
        board_id=column_in.board_id,
    )
    db.add(new_column)
    await db.commit()
    await db.refresh(new_column)
    return new_column


@router.get("/", response_model=list[ColumnRead])
async def list_columns(
    board_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Column).join(Board).where(Board.owner_id == current_user.id)
    if board_id is not None:
        query = query.where(Column.board_id == board_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{column_id}", response_model=ColumnRead)
async def get_column(column: Column = Depends(get_owned_column)):
    return column


@router.put("/{column_id}", response_model=ColumnRead)
async def update_column(
    column_in: ColumnCreate,
    column: Column = Depends(get_owned_column),
    db: AsyncSession = Depends(get_db),
):
    column.name = column_in.name
    column.position = column_in.position
    column.board_id = column_in.board_id

    await db.commit()
    await db.refresh(column)
    return column


@router.delete("/{column_id}", status_code=204)
async def delete_column(
    column: Column = Depends(get_owned_column),
    db: AsyncSession = Depends(get_db),
):
    await db.delete(column)
    await db.commit()