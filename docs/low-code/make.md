# Make Mapping

Typical mapping:

- Webhook trigger -> capture invoice metadata
- HTTP module -> call `/validate` or `/run`
- Router module -> branch on approved, review, or rejected
- Data store or task module -> preserve review packet IDs and notes

The local workflow focuses on payload shape and route semantics, not live module setup.
