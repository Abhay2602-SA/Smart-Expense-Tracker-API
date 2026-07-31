# Smart Expense Tracker API

A REST API for managing personal expenses: add, view, filter by category,
calculate totals, and delete. Built with FastAPI and an in-memory store.

## Features

- `GET /` — friendly landing message (points you to `/docs`)
- `POST /expenses` — add an expense (title, amount, category, date)
- `GET /expenses` — view all expenses
- `GET /expenses?category=Food` — filter by category
- `GET /expenses/total` — overall total + breakdown by category
- `GET /expenses/total?category=Food` — total for one category
- `DELETE /expenses/{id}` — delete an expense
- `GET /docs` — **bonus:** interactive Swagger/OpenAPI docs (auto-generated
  by FastAPI — chosen as the single optional bonus per the assignment)

Tests run automatically on every push via GitHub Actions
(`.github/workflows/tests.yml`).

## Install

```bash

environment setup :
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

main step :
pip install -r requirements.txt
```

## Run the server

```bash
uvicorn src.main:app --reload
```

Server runs at `http://127.0.0.1:8000`. Interactive docs at
`http://127.0.0.1:8000/docs`.

## Run tests

```bash
pytest
```

## Example usage

```bash
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee", "amount": 4.5, "category": "Food", "date": "2026-07-01"}'

curl http://127.0.0.1:8000/expenses?category=Food

curl http://127.0.0.1:8000/expenses/total
```

## Design notes

- Data is stored in memory (a dict keyed by generated UUID) and resets on
  restart — no database required per the assignment.
- `amount` must be > 0 and `title`/`category` must be non-empty; invalid
  input returns `422` via Pydantic validation.
- Deleting a nonexistent id returns `404`.
- Storage logic lives in `src/storage.py`, separate from the route handlers
  in `src/main.py`, so the in-memory store could be swapped for a JSON file
  or database later without touching the API layer.
- Only one optional bonus was implemented (Swagger/OpenAPI docs), per the
  assignment's "pick at most one" instruction.
