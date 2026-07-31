import pytest
from fastapi.testclient import TestClient

from src.main import app, store

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    """Each test gets a clean store, since it's a module-level singleton."""
    store._expenses.clear()
    yield
    store._expenses.clear()


def _add(title="Coffee", amount=4.5, category="Food", date="2026-07-01"):
    return client.post(
        "/expenses",
        json={"title": title, "amount": amount, "category": category, "date": date},
    )


def test_add_expense_returns_created_expense_with_id():
    response = _add()
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Coffee"
    assert data["amount"] == 4.5
    assert "id" in data and data["id"]


def test_add_expense_rejects_non_positive_amount():
    response = _add(amount=-5)
    assert response.status_code == 422


def test_add_expense_rejects_empty_title():
    response = _add(title="")
    assert response.status_code == 422


def test_list_expenses_empty_initially():
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == []


def test_list_expenses_returns_all():
    _add(title="Coffee", category="Food")
    _add(title="Bus", category="Transport")
    response = client.get("/expenses")
    assert len(response.json()) == 2


def test_filter_by_category():
    _add(title="Coffee", category="Food")
    _add(title="Bus", category="Transport")
    response = client.get("/expenses", params={"category": "Food"})
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Coffee"


def test_filter_by_category_is_case_insensitive():
    _add(title="Coffee", category="Food")
    response = client.get("/expenses", params={"category": "food"})
    assert len(response.json()) == 1


def test_total_overall_and_by_category():
    _add(title="Coffee", amount=4.5, category="Food", date="2026-07-01")
    _add(title="Bus", amount=2.0, category="Transport", date="2026-07-02")
    response = client.get("/expenses/total")
    data = response.json()
    assert data["overall_total"] == 6.5
    assert data["by_category"] == {"Food": 4.5, "Transport": 2.0}


def test_total_for_specific_category():
    _add(title="Coffee", amount=4.5, category="Food", date="2026-07-01")
    _add(title="Lunch", amount=10.0, category="Food", date="2026-07-02")
    _add(title="Bus", amount=2.0, category="Transport", date="2026-07-02")
    response = client.get("/expenses/total", params={"category": "Food"})
    assert response.json()["total"] == 14.5


def test_delete_expense_removes_it():
    created = _add().json()
    response = client.delete(f"/expenses/{created['id']}")
    assert response.status_code == 204
    assert client.get("/expenses").json() == []


def test_delete_nonexistent_expense_returns_404():
    response = client.delete("/expenses/does-not-exist")
    assert response.status_code == 404


def test_root_endpoint_does_not_404():
    response = client.get("/")
    assert response.status_code == 200


def test_filter_by_nonexistent_category_returns_empty_list():
    _add(title="Coffee", category="Food")
    response = client.get("/expenses", params={"category": "Nonexistent"})
    assert response.status_code == 200
    assert response.json() == []


def test_total_by_category_sums_multiple_expenses_in_same_category():
    _add(title="Coffee", amount=4.5, category="Food", date="2026-07-01")
    _add(title="Lunch", amount=12.0, category="Food", date="2026-07-02")
    _add(title="Dinner", amount=20.0, category="Food", date="2026-07-03")
    response = client.get("/expenses/total")
    data = response.json()
    assert data["by_category"]["Food"] == 36.5


def test_total_with_no_expenses_is_zero():
    response = client.get("/expenses/total")
    data = response.json()
    assert data["overall_total"] == 0
    assert data["by_category"] == {}

