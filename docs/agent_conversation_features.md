# Agent Conversation & Eval — Feature Design

## 1. Customizable Parent Prompt

**Scope**: Backend script + API

Currently `create_session()` loads parent profiles from `resources/parent_profiles/*.txt` files. The coach prompt is already customizable via `--coach-prompt` / `--coach-prompt-file`.

**Change**: Allow the same for the parent side.

- Script: add `--parent-prompt` / `--parent-prompt-file` args (mutually exclusive with `--parent-profile-id`)
- API: accept optional `parent_prompt` field in the run request body
- When a custom parent prompt is provided, skip `parent_profile_service` entirely and pass it directly to `create_session(parent_profile=...)`
- Output JSON: record `"parent_profile": "custom"` when a user-supplied prompt is used

## 2. No Timeout on Generation & Eval

**Scope**: Backend API (+ frontend awareness)

Conversation generation (multiple LLM round-trips) and 3-dimension evaluation can take 2–10+ minutes. HTTP request timeouts or worker timeouts must not kill the process.

- API layer: do **not** set a request timeout on the generation endpoint
- ASGI config: ensure `uvicorn --timeout-keep-alive` and any reverse proxy (nginx `proxy_read_timeout`) are set high enough or disabled for this endpoint
- Script: already runs via `asyncio.run()` with no timeout — no change needed
- Frontend: must not use a short `fetch` timeout; see Feature 3

## 3. Async Task UX (Frontend + Backend)

**Scope**: Frontend (primary), Backend API

Generation is intrinsically long-running. The UX should treat it as an async task, not a synchronous request-response.

### Backend

- **Task creation endpoint**: `POST /api/v1/coach/runs` returns immediately with a `run_id` and status `"pending"`
- **Background execution**: the actual conversation + eval runs in a background worker (e.g. FastAPI `BackgroundTasks`, or a task queue like Celery/ARQ if scaling is needed)
- **Status polling endpoint**: `GET /api/v1/coach/runs/{run_id}` returns current status (`pending` → `running` → `completed` | `failed`), progress info (current turn / total turns, which eval dimension is running), and the result when done
- **Result stored in DB**: conversation + eval JSON saved to `coach_run` table so it persists beyond the request lifecycle

### Frontend

- User clicks "Generate" → gets a confirmation with the `run_id`, UI shows a task card with status "Running..."
- User can navigate away; the task card persists in a sidebar / task list
- Polling or SSE updates the card: "Turn 2/5...", "Evaluating TES...", "Done ✓"
- When complete, user clicks to view results (conversation + eval viewer)
- No loading spinner blocking the whole UI — the generation is a background job the user checks on

### Sequence

```
User                    Frontend                  Backend
 |-- Click Generate -->  |                         |
 |                       |-- POST /runs ---------->|
 |                       |<-- 201 {run_id} --------|
 |<-- Show task card --- |                         |-- spawn background task
 |                       |                         |   (conversation + eval)
 |   (user does          |                         |
 |    other things)      |-- GET /runs/{id} ------>|
 |                       |<-- {status: running} ---|
 |                       |-- GET /runs/{id} ------>|
 |                       |<-- {status: completed,  |
 |                       |     result: {...}} -----|
 |<-- Show results ----- |                         |
```
