# API

Invoice Router exposes a local FastAPI surface for the fixture-safe proof bundle.

## Endpoints

- `GET /health`
- `GET /scenarios`
- `POST /validate`
- `POST /run`
- `GET /runs/{id}`
- `POST /queue/claim`
- `POST /queue/resolve`

## Health contract

```json
{
  "status": "ok",
  "fixture_safe": true,
  "live_services_used": false,
  "synthetic_data_only": true
}
```

## Example requests

Run the clean approval scenario:

```bash
curl -fsS -X POST http://127.0.0.1:8024/run   -H 'Content-Type: application/json'   --data @examples/api-requests/run-clean-approved-invoice.json
```

Validate the arithmetic-mismatch scenario:

```bash
curl -fsS -X POST http://127.0.0.1:8024/validate   -H 'Content-Type: application/json'   --data @examples/api-requests/validate-mismatched-total.json
```
