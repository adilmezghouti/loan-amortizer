from pydantic import BaseModel
import datetime


class User(BaseModel):
    first_name: str
    last_name: str


class Loan(BaseModel):
    principal: float
    interest_rate: float
    term: int