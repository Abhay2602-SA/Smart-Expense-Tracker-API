# AI Notes

## Which parts were AI-generated vs. written by me

I used Claude to generate the full first draft of this project — the models
(`src/models.py`), the storage layer (`src/storage.py`), the API routes
(`src/main.py`), the test suite (`tests/test_expenses.py`), the README, and
the CI workflow. I didn't hand-write the initial code myself; I described
the requirements from the assignment email and had Claude build it, then
went through the result rather than accepting it blind.

I did make the actual decisions along the way — what stack to use (FastAPI),
which single bonus to keep, what to cut, and what extra polish was worth
adding. Those choices are mine even though the code implementing them was
AI-written.

## What I validated, tested, or changed, and why

- Ran `pytest` myself on my own machine (not just trusting that it "should"
  work) — all 15 tests pass.
- Started the server locally with `uvicorn src.main:app --reload` and
  manually exercised every endpoint through the Swagger UI at `/docs`:
  added an expense, listed all expenses, filtered by category, checked the
  total, and deleted an expense — confirming the response codes (201, 200,
  204, 404) actually match what the code claims to do.
- Hit `/` in the browser early on and got a 404, which confused me at
  first — turned out that route just wasn't defined. I had it add a proper
  `GET /` endpoint so that's no longer a dead end for anyone reviewing this.
- Asked for a few extra edge-case tests beyond the happy path: filtering by
  a category that doesn't exist (should return an empty list, not error),
  totals when multiple expenses share a category, and totals when there's
  no data yet.
- After reading `src/main.py` and `src/storage.py`, I like that the storage
  logic is separated from the routes. It keeps the API layer focused on
  handling requests and makes the data layer easier to swap out or test later.
  I’d still keep the UUID-based IDs, since they avoid collisions and feel a bit
  more solid than simple integer IDs for a small API like this.

## AI suggestions I decided not to use, and why

- The assignment says to pick *at most one* optional bonus. I had Claude
  generate all four initially (search, monthly summary, Swagger docs,
  Docker) but cut it back to just Swagger/OpenAPI docs — it's the only one
  that's essentially free (FastAPI generates it automatically, so it adds
  no extra code or bug surface), and it gives a genuinely interactive way
  to demo the API without going outside the assignment's scope.
- I also considered building a fancier 3D/animated frontend to make the
  submission "stand out," but decided against it — this is a backend API
  assignment reviewed by an automated process that runs the README's exact
  commands, so a frontend wouldn't even be seen by the grader, and it risks
  reading as not understanding the assignment's scope rather than as
  initiative. Instead I kept a small optional `api-console.html` — a plain
  local tool for manually testing the endpoints, clearly separate from the
  graded deliverable, not counted as the bonus.
- Skipped switching from in-memory storage to a JSON file, even though the
  assignment allows either — in-memory is simpler, fully compliant, and I
  didn't see a reason to add file I/O complexity without a clear benefit.
