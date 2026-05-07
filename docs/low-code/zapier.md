# Zapier Mapping

Typical mapping:

- Catch Hook trigger -> receive invoice payload metadata
- Webhooks by Zapier action -> call `/run`
- Paths step -> branch on `routing_outcome`
- Storage or task action -> keep review packet IDs and operator notes

The local workflow documents a safe request and response contract without claiming live connector execution.
