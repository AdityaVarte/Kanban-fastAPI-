from pydantic import BaseModel, ConfigDict


class CardBase(BaseModel):
    title: str
    description: str | None = None
    position: int = 0


class CardCreate(CardBase):
    column_id: int


class CardRead(CardBase):
    id: int
    column_id: int

    model_config = ConfigDict(from_attributes=True)
    
class CardMove(BaseModel):
    column_id: int
    position: int