"""Formatters: transform a token list into various output styles."""
import difflib

# Readable POS abbreviations (Penn Treebank → short label)
_ABBREV: dict[str, str] = {
    "NN": "n",   "NNS": "n",   "NNP": "n",   "NNPS": "n",
    "VB": "v",   "VBD": "v",   "VBG": "v",   "VBN": "v",  "VBP": "v", "VBZ": "v",
    "MD": "v",
    "JJ": "adj", "JJR": "adj", "JJS": "adj",
    "RB": "adv", "RBR": "adv", "RBS": "adv",
    "DT": "det", "PDT": "det",
    "IN": "prep",
    "CC": "conj",
    "PRP": "pn", "PRP$": "pn", "WP": "pn", "WP$": "pn",
    "TO": "to",
    "EX": "ex",
    "RP": "part",
    "UH": "int",
    "CD": "num",
    "WDT": "rel", "WRB": "rel",
    "FW": "fw",
    "POS": "poss",
}

Token = tuple[str, str | None]
Tokens = list[Token]


def _abbrev(tag: str) -> str:
    return _ABBREV.get(tag, "?")


# ── Plain (default) ──────────────────────────────────────────────────────────

def plain(tokens: Tokens, position: str = "prefix", sep: str = "_") -> str:
    """Annotate each word with its readable POS abbreviation."""
    parts = []
    for seg, tag in tokens:
        if tag:
            abbrev = _abbrev(tag)
            parts.append(f"{abbrev}{sep}{seg}" if position == "prefix" else f"{seg}{sep}{abbrev}")
        else:
            parts.append(seg)
    return "".join(parts)


# ── Parse tree (debug) ───────────────────────────────────────────────────────

def parse_tree(tokens: Tokens) -> str:
    """Tabular debug view showing each segment, its type, and POS tag."""
    col = (24, 8, 8, 6)
    header = (
        f"{'SEGMENT':<{col[0]}} {'TYPE':<{col[1]}} {'POS':<{col[2]}} {'ABBREV'}"
    )
    sep = "  ".join("-" * w for w in col)
    rows = [header, sep]
    for seg, tag in tokens:
        display = repr(seg) if (not seg.strip() or "\n" in seg) else seg
        if tag:
            rows.append(
                f"{display:<{col[0]}} {'word':<{col[1]}} {tag:<{col[2]}} {_abbrev(tag)}"
            )
        else:
            kind = "space" if seg.isspace() else "punct"
            rows.append(
                f"{display:<{col[0]}} {kind:<{col[1]}} {'—':<{col[2]}} —"
            )
    return "\n".join(rows) + "\n"


# ── Original text (cat passthrough) ─────────────────────────────────────────

def original_text(text: str) -> str:
    """Return the input text unchanged — no parsing, pure passthrough."""
    return text


# ── Parse-and-reconstruct (round-trip) ──────────────────────────────────────

def parse_and_reconstruct(tokens: Tokens) -> str:
    """Reconstruct text from the parse tree. Identical to original_text iff
    the tokenizer is lossless. Use alongside original_text to verify."""
    return "".join(seg for seg, _ in tokens)


# ── Regenerated (alias for parse_and_reconstruct) ───────────────────────────

def regenerated(tokens: Tokens) -> str:
    """Alias for parse_and_reconstruct (kept for backward compatibility)."""
    return parse_and_reconstruct(tokens)


# ── Raw NLTK tags ────────────────────────────────────────────────────────────

def raw_nltk(tokens: Tokens, position: str = "prefix", sep: str = "_") -> str:
    """Annotate each word with its raw NLTK Penn Treebank tag."""
    parts = []
    for seg, tag in tokens:
        if tag:
            parts.append(f"{tag}{sep}{seg}" if position == "prefix" else f"{seg}{sep}{tag}")
        else:
            parts.append(seg)
    return "".join(parts)


# ── HN CamelCase ─────────────────────────────────────────────────────────────

def camel(tokens: Tokens, position: str = "prefix") -> str:
    """Hungarian Notation CamelCase: prefix→adjHonorable/nFriends, postfix→honorableAdj/friendsN."""
    parts = []
    for seg, tag in tokens:
        if tag:
            abbrev = _abbrev(tag)
            if position == "prefix":
                parts.append(f"{abbrev.lower()}{seg[0].upper()}{seg[1:]}")
            else:
                parts.append(f"{seg}{abbrev.capitalize()}")
        else:
            parts.append(seg)
    return "".join(parts)


# ── HTML (all 4 view modes) ──────────────────────────────────────────────────

def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace("\n", "<br>\n")
    )


def html(tokens: Tokens, position: str = "prefix", sep: str = "_") -> str:
    """Full HTML page with 4 CSS view modes and JS toggle buttons."""
    parts = []
    for seg, tag in tokens:
        if not tag:
            parts.append(_esc(seg))
        else:
            abbrev = _abbrev(tag)
            word_span = f'<span class="w pos-{abbrev}">{_esc(seg)}</span>'
            if position == "prefix":
                tag_span = f'<span class="pt">{abbrev}{sep}</span>'
                parts.append(f'<span class="wg">{tag_span}{word_span}</span>')
            else:
                tag_span = f'<span class="pt">{sep}{abbrev}</span>'
                parts.append(f'<span class="wg">{word_span}{tag_span}</span>')
    body = "".join(parts)
    return _HTML_TEMPLATE.format(body=body)


_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>pos-decorate output</title>
<style>
  body {{ font-family: Georgia, serif; max-width: 700px; margin: 2em auto; line-height: 1.8; }}
  .controls {{ margin-bottom: 1.5em; display: flex; gap: 0.5em; flex-wrap: wrap; }}
  button {{ padding: 0.4em 0.9em; cursor: pointer; border: 1px solid #888;
            border-radius: 3px; background: #f5f5f5; font-family: inherit; }}
  button.active {{ background: #222; color: #fff; border-color: #222; }}

  /* Mode: As Written (default) */
  .mode-as-written .pt {{ display: none; }}

  /* Mode: POS-Tagged */
  .mode-pos-tagged .pt {{ display: inline; color: #000; }}
  .mode-pos-tagged .w  {{ color: #000; }}

  /* Mode: Tag-Receding */
  .mode-tag-receding .pt {{ display: inline; color: #bbb; font-size: 0.78em; }}
  .mode-tag-receding .w  {{ color: #000; font-weight: 600; }}

  /* Mode: Grammar-Lit (no tags, words colored by POS) */
  .mode-grammar-lit .pt      {{ display: none; }}
  .mode-grammar-lit .pos-n   {{ color: #1a56db; }}
  .mode-grammar-lit .pos-v   {{ color: #057a55; }}
  .mode-grammar-lit .pos-adj {{ color: #9f1ab1; }}
  .mode-grammar-lit .pos-adv {{ color: #c27803; }}
  .mode-grammar-lit .pos-det {{ color: #6b7280; }}
  .mode-grammar-lit .pos-prep {{ color: #6b7280; }}
  .mode-grammar-lit .pos-conj {{ color: #6b7280; }}
  .mode-grammar-lit .pos-pn  {{ color: #e02424; }}
  .mode-grammar-lit .pos-to  {{ color: #6b7280; }}
</style>
</head>
<body>
<div class="controls">
  <button onclick="setMode('as-written')"   id="btn-as-written"   class="active">As Written</button>
  <button onclick="setMode('pos-tagged')"   id="btn-pos-tagged">POS-Tagged</button>
  <button onclick="setMode('tag-receding')" id="btn-tag-receding">Tag-Receding</button>
  <button onclick="setMode('grammar-lit')"  id="btn-grammar-lit">Grammar-Lit</button>
</div>
<div id="text" class="mode-as-written">
{body}
</div>
<script>
function setMode(mode) {{
  document.getElementById('text').className = 'mode-' + mode;
  document.querySelectorAll('.controls button').forEach(function(b) {{
    b.classList.remove('active');
  }});
  document.getElementById('btn-' + mode).classList.add('active');
}}
</script>
</body>
</html>"""


# ── Verify round-trip ────────────────────────────────────────────────────────

def verify_round_trip(original: str, tokens: Tokens) -> tuple[bool, str]:
    """Check that regenerated text matches original exactly.

    Returns (is_clean, diff_text). diff_text is empty when is_clean is True.
    """
    rebuilt = regenerated(tokens)
    if original == rebuilt:
        return True, ""
    diff = "".join(
        difflib.unified_diff(
            original.splitlines(keepends=True),
            rebuilt.splitlines(keepends=True),
            fromfile="original",
            tofile="regenerated",
        )
    )
    return False, diff
