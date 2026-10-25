from pydantic import BaseModel, ConfigDict


class ColumnBase(BaseModel):
    name: str
    position: int = 0


class ColumnCreate(ColumnBase):
    board_id: int


class ColumnRead(ColumnBase):
    id: int
    board_id: int

    model_config = ConfigDict(from_attributes=True)