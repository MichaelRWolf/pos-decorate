# pos-decorate — Claude Context

## Project

General-purpose CLI tool: ingest English text, output POS-decorated in multiple styles.
Part of a two-repo project; the companion piece is `honor-hungarian-notation`.

## Plan File

`~/.claude/plans/i-have-long-wanted-compiled-robin.md`

## Phase Status

Phase 4 (pos-decorate CLI) is complete. See `honor-hungarian-notation/CLAUDE.md`
for the full phase table and next steps (Phase 5 — blog post).

## Resume

Open `~/repos/honor-hungarian-notation` — that repo's `CLAUDE.md` is the primary
re-entry point. Say `continue` for Phase 5.

## Key Decisions

- POS prefix style: readable abbreviations (`n_`, `v_`, `adj_`) by default; `--style` flag for variants
- Tokenizer is lossless: regex `[A-Za-z']+|[^A-Za-z']+`; whitespace and punctuation pass through unchanged
- NLTK Penn Treebank tagset; spaCy not used (unavailable on Python 3.14)
- All code fresh — prior-art repos are reference only

## Running Tests

```bash
source venv/bin/activate
pytest
```

Three approval tests in `tests/test_parse_tree.py`:

- `test_roses_are_red` — classic poem; nouns, verbs, adjectives, contraction
- `test_comprehensive_coverage` — all POS categories, punctuation, whitespace
- `test_parse_print_round_trip` — asserts tokenizer is lossless (round-trip identity)

Approved files live alongside the tests (`*.approved.txt`).
To approve new output: copy the received file to the approved path shown in the error.
Never auto-approve — always review the diff first.
