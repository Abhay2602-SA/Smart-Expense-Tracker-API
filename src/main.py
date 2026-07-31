from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .models import Expense, ExpenseCreate
from .storage import ExpenseStore

app = FastAPI(
    title="Smart Expense Tracker API",
    description="A REST API for tracking personal expenses.",
    version="1.0.0",
    # /docs and /openapi.json are generated automatically by FastAPI —
    # this satisfies the "OpenAPI/Swagger docs" bonus with no extra code.
)

# Allows a locally-opened HTML page (different origin) to call this API.
# Fine for local development/testing; not something a production API would do.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

store = ExpenseStore()


@app.get("/")
def root():
    """Friendly landing response so the bare URL doesn't 404 — see /docs for the API."""
    return {"message": "Smart Expense Tracker API is running. See /docs for interactive API docs."}


@app.post("/expenses", response_model=Expense, status_code=201)
def add_expense(expense: ExpenseCreate) -> Expense:
    """Add a new expense."""
    return store.add(expense)


@app.get("/expenses", response_model=List[Expense])
def list_expenses(
    category: Optional[str] = Query(None, description="Filter by category"),
) -> List[Expense]:
    """View all expenses, optionally filtered by category."""
    return store.get_all(category=category)


@app.get("/expenses/total")
def get_total(
    category: Optional[str] = Query(
        None, description="If provided, totals only this category. Otherwise returns overall + per-category totals."
    )
):
    """Calculate total expenses, overall or for one category."""
    if category:
        return {"category": category, "total": store.total(category=category)}
    return {"overall_total": store.total(), "by_category": store.total_by_category()}


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: str) -> None:
    """Delete an expense by id."""
    if not store.delete(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return None
