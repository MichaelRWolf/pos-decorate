# pos-decorate — Claude Context

## Project
General-purpose CLI tool: ingest English text, output POS-decorated in 4 styles.
Part of a two-repo project; the companion piece is `honor-hungarian-notation`.

## Plan File
`~/.claude/plans/i-have-long-wanted-compiled-robin.md`

## Current Phase
Phase 4 — implement `pos-decorate` CLI (Tokenizer → Formatter → Assembler pipeline)

## Resume
Say `continue` to pick up from the first unchecked box in the plan file.

## Key Decisions
- POS prefix style: readable abbreviations (`n_`, `v_`, `adj_`) by default; `--style` flag for variants
- Tokenizer must be lossless: preserve whitespace, line breaks, and punctuation unchanged
- spaCy preferred over NLTK for whitespace preservation (`token.whitespace_`)
- All code fresh — do not build on prior-art repos (reference only)
