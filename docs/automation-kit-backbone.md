# Optional Shared-Convention Boundary

Invoice Router is fully usable on its own. It does not require any other repository in order to run the local proof bundle.

When shared conventions are useful, this repo can borrow the following ideas without taking a hard dependency on them:

- `automation-kit` for reusable local proof conventions and capability metadata shape;
- `review-router` for review queue discipline and replayable artifact layout;
- `sheets-airtable-sync` for typed output mapping and evidence packaging.

Boundary rules:

- keep Invoice Router runnable from a clean checkout;
- do not hide core behavior behind undeclared external repo imports;
- treat any shared import as optional and import-safe;
- keep the invoice domain logic here.
