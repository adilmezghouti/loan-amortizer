from pydantic import BaseModel
import datetime


class User(BaseModel):
    email: str
    first_name: str
    last_name: str


class Loan(BaseModel):
    principal: float
    interest_rate: float
    term: int


class Sharing(BaseModel):
    sharer_id: int
    shared_with_id: int
