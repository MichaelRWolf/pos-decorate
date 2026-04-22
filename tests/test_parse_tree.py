"""Approval tests for parse tree output.

These tests verify that the NL parser (NLTK) produces the expected POS tags
for known inputs. The approved files capture the full parse tree — segment,
type, raw NLTK tag, and readable abbreviation — so any change in tagging
behavior or tag mapping is caught explicitly.

Testing the parse tree (not reconstructed text) ensures the test cannot be
satisfied by a trivial pass-through implementation.
"""
from approvaltests import verify

from pos_decorate.tokenizer import tokenize
from pos_decorate.formatter import parse_tree, original_text, parse_and_reconstruct

# Shared input for coverage tests — keep in sync with test_parse_print_round_trip
_COMPREHENSIVE = (
    # adverbs + preposition + pronoun
    "She quickly ran over the bridge.\n"
    # interjection + pronoun + adverb + verb
    "Oh! He never said why.\n"
    # number + conjunction
    "I have 42 reasons and one excuse.\n"
    # possessive + em-dash + semicolon + colon
    "Caesar's ambition—a grievous fault; consider: was it so?\n"
    # parentheses + quotation marks
    'He spoke (or rather shouted): "Friends!"\n'
    # tab indentation + multiple spaces
    "\tIndented  line.\n"
)


def test_roses_are_red():
    """Classic poem — nouns, verbs, adjectives, determiner, contraction.

    Notable: 'doesn't' is a contraction; the apostrophe-inclusive tokenizer
    keeps it as one token. NLTK tags it as a single unit.
    """
    text = (
        "Roses are red.\n"
        "Violets are blue.\n"
        "Some poems rhyme.\n"
        "This one doesn't.\n"
    )
    verify(parse_tree(tokenize(text)))


def test_comprehensive_coverage():
    """Exercises POS categories, punctuation, and whitespace not in the poem.

    Coverage added beyond the poem:
      adv    — quickly, never
      prep   — over, into
      conj   — and, but
      pn     — I, he, she, they
      int    — Oh
      num    — 42, one
      poss   — Caesar's
      punct  — , ; : ( ) — ! ? " ...
      space  — tab (\\t), multiple spaces
    """
    verify(parse_tree(tokenize(_COMPREHENSIVE)))


def test_parse_print_round_trip():
    """original-text and parse-and-reconstruct produce identical output.

    Verifies that the tokenizer is lossless: every character in the input
    survives the parse → reconstruct cycle unchanged.
    """
    tokens = tokenize(_COMPREHENSIVE)
    assert original_text(_COMPREHENSIVE) == parse_and_reconstruct(tokens)
