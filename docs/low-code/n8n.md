# n8n Mapping

Typical mapping:

- Trigger node -> receive invoice upload event
- HTTP Request / Code node -> call `/run`
- IF node -> branch on `routing_outcome`
- Approved path -> forward export preview payload
- Review path -> post the packet ID into a human review lane

Placeholder credentials only. Keep live endpoints disabled in the default proof.
