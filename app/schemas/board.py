from pydantic import BaseModel, ConfigDict


class BoardBase(BaseModel):
    name: str


class BoardCreate(BoardBase):
    pass


class BoardRead(BoardBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ColumnNested(BaseModel):
    id: int
    name: str
    position: int

    model_config = ConfigDict(from_attributes=True)


class CardNested(BaseModel):
    id: int
    title: str
    description: str | None = None
    position: int

    model_config = ConfigDict(from_attributes=True)


class ColumnWithCards(ColumnNested):
    cards: list[CardNested] = []


class BoardWithColumns(BoardRead):
    columns: list[ColumnWithCards] = []