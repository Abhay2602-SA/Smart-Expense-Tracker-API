import uuid
from typing import Dict, List, Optional

from .models import Expense, ExpenseCreate


class ExpenseStore:
    """Simple in-memory store. Swappable later for a JSON file or DB without
    touching the route handlers, since main.py only talks to this interface."""

    def __init__(self) -> None:
        self._expenses: Dict[str, Expense] = {}

    def add(self, data: ExpenseCreate) -> Expense:
        expense_id = str(uuid.uuid4())
        expense = Expense(id=expense_id, **data.model_dump())
        self._expenses[expense_id] = expense
        return expense

    def get_all(self, category: Optional[str] = None) -> List[Expense]:
        results = list(self._expenses.values())
        if category:
            results = [e for e in results if e.category.lower() == category.lower()]
        return sorted(results, key=lambda e: e.date)

    def delete(self, expense_id: str) -> bool:
        if expense_id in self._expenses:
            del self._expenses[expense_id]
            return True
        return False

    def total(self, category: Optional[str] = None) -> float:
        expenses = self.get_all(category=category)
        return round(sum(e.amount for e in expenses), 2)

    def total_by_category(self) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        for e in self._expenses.values():
            totals[e.category] = round(totals.get(e.category, 0) + e.amount, 2)
        return totals
