"""Lossless tokenizer: splits text into (segment, pos_tag) pairs.

Words receive a POS tag from NLTK. Non-word segments (punctuation, whitespace,
line breaks) receive None. Joining all segments reconstructs the original text
exactly — no characters lost.
"""
import re
from nltk import pos_tag

_SEGMENT_RE = re.compile(r"[A-Za-z']+|[^A-Za-z']+")


def _ensure_tagger() -> None:
    """Download NLTK POS tagger data if not already present."""
    try:
        pos_tag(["test"])
    except LookupError:
        import nltk
        # Try newer package name first, fall back to legacy name
        for pkg in ("averaged_perceptron_tagger_eng", "averaged_perceptron_tagger"):
            try:
                nltk.download(pkg, quiet=True)
                pos_tag(["test"])
                return
            except LookupError:
                continue


def tokenize(text: str) -> list[tuple[str, str | None]]:
    """Return a list of (segment, pos_tag) pairs for the given text.

    - Word segments: alphabetic runs; pos_tag is an NLTK Penn Treebank tag.
    - Non-word segments: everything else; pos_tag is None.
    - ''.join(seg for seg, _ in result) == text  (guaranteed lossless)
    """
    _ensure_tagger()
    segments = _SEGMENT_RE.findall(text)

    words = [s for s in segments if s[0].isalpha()]
    tagged_words = pos_tag(words) if words else []
    word_tag_iter = iter(tagged_words)

    result: list[tuple[str, str | None]] = []
    for seg in segments:
        if seg[0].isalpha():
            _, tag = next(word_tag_iter)
            result.append((seg, tag))
        else:
            result.append((seg, None))
    return result
