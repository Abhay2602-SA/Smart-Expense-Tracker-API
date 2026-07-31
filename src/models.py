from datetime import date as date_type

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """Fields required to create a new expense. `id` is generated server-side."""

    title: str = Field(..., min_length=1, description="Short description of the expense")
    amount: float = Field(..., gt=0, description="Must be a positive number")
    category: str = Field(..., min_length=1, description="e.g. Food, Transport, Housing")
    date: date_type = Field(..., description="Date the expense occurred, YYYY-MM-DD")


class Expense(ExpenseCreate):
    """An expense as stored/returned by the API, including its generated id."""

    id: str
