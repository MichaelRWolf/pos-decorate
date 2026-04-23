"""Unit tests for --prefix / --postfix position and separator combinations.

These test the formatter functions directly — no approval files needed,
since the outputs are short and fully deterministic.
"""
import pytest

from pos_decorate.formatter import plain, raw_nltk, camel

# (word, tag), punctuation passthrough, (word, tag)
_TOKENS = [("Friends", "NNS"), (", ", None), ("come", "VBP")]


@pytest.mark.parametrize("position,sep,expected", [
    ("prefix",  "_",  "n_Friends, v_come"),
    ("prefix",  "-",  "n-Friends, v-come"),
    ("prefix",  " ",  "n Friends, v come"),
    ("prefix",  "",   "nFriends, vcome"),
    ("postfix", "_",  "Friends_n, come_v"),
    ("postfix", "-",  "Friends-n, come-v"),
    ("postfix", " ",  "Friends n, come v"),
    ("postfix", "",   "Friendsn, comev"),
])
def test_plain(position, sep, expected):
    assert plain(_TOKENS, position=position, sep=sep) == expected


@pytest.mark.parametrize("position,sep,expected", [
    ("prefix",  "_",  "NNS_Friends, VBP_come"),
    ("prefix",  "-",  "NNS-Friends, VBP-come"),
    ("prefix",  "",   "NNSFriends, VBPcome"),
    ("postfix", "_",  "Friends_NNS, come_VBP"),
    ("postfix", "-",  "Friends-NNS, come-VBP"),
    ("postfix", "",   "FriendsNNS, comeVBP"),
])
def test_raw_nltk(position, sep, expected):
    assert raw_nltk(_TOKENS, position=position, sep=sep) == expected


@pytest.mark.parametrize("position,expected", [
    ("prefix",  "nFriends, vCome"),
    ("postfix", "FriendsN, comeV"),
])
def test_camel(position, expected):
    # camel has no sep — capitalisation is the delimiter
    assert camel(_TOKENS, position=position) == expected


def test_punctuation_passthrough():
    """Non-word tokens are never annotated regardless of position/sep."""
    tokens = [(".", None), (" ", None), ("!", None)]
    assert plain(tokens, position="postfix", sep="-") == ". !"
    assert raw_nltk(tokens, position="postfix", sep="-") == ". !"
    assert camel(tokens, position="postfix") == ". !"
