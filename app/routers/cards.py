from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_owned_column_by_id
from app.schemas.card import CardMove

from app.db.session import get_db
from app.core.deps import get_current_user, get_owned_card
from app.models import Card, Column, Board, User
from app.schemas.card import CardCreate, CardRead

router = APIRouter(prefix="/cards", tags=["cards"])


@router.post("/", response_model=CardRead, status_code=201)
async def create_card(
    card_in: CardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    column = await db.get(Column, card_in.column_id)
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")

    board = await db.get(Board, column.board_id)
    if board is None or board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add cards to this column")

    new_card = Card(
        title=card_in.title,
        description=card_in.description,
        position=card_in.position,
        column_id=card_in.column_id,
    )
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card


@router.get("/", response_model=list[CardRead])
async def list_cards(
    column_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Card).join(Column).join(Board).where(Board.owner_id == current_user.id)
    if column_id is not None:
        query = query.where(Card.column_id == column_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{card_id}", response_model=CardRead)
async def get_card(card: Card = Depends(get_owned_card)):
    return card


@router.put("/{card_id}", response_model=CardRead)
async def update_card(
    card_in: CardCreate,
    card: Card = Depends(get_owned_card),
    db: AsyncSession = Depends(get_db),
):
    card.title = card_in.title
    card.description = card_in.description
    card.position = card_in.position
    card.column_id = card_in.column_id

    await db.commit()
    await db.refresh(card)
    return card


@router.delete("/{card_id}", status_code=204)
async def delete_card(
    card: Card = Depends(get_owned_card),
    db: AsyncSession = Depends(get_db),
):
    await db.delete(card)
    await db.commit()
    
    

@router.patch("/{card_id}/move", response_model=CardRead)
async def move_card(
    card_in: CardMove,
    card: Card = Depends(get_owned_card),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    target_column = await get_owned_column_by_id(card_in.column_id, db, current_user)

    old_column_id = card.column_id
    card.column_id = target_column.id
    card.position = card_in.position
    await db.flush()

    # Re-sequence the target column's cards around the moved card
    result = await db.execute(
        select(Card).where(Card.column_id == target_column.id).order_by(Card.position, Card.id)
    )
    siblings = [c for c in result.scalars().all() if c.id != card.id]
    siblings.insert(card_in.position, card)

    for index, sibling in enumerate(siblings):
        sibling.position = index

    # If moved out of a different column, re-sequence what's left behind
    if old_column_id != target_column.id:
        result = await db.execute(
            select(Card).where(Card.column_id == old_column_id).order_by(Card.position, Card.id)
        )
        for index, sibling in enumerate(result.scalars().all()):
            sibling.position = index

    await db.commit()
    await db.refresh(card)
    return card