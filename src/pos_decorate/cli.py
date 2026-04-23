"""pos-decorate: decorate English text with Part-of-Speech annotations."""
import argparse
import sys

from pos_decorate.tokenizer import tokenize
from pos_decorate import formatter as fmt


_STYLES = [
    "plain",
    "parse-tree",
    "original-text",
    "parse-and-reconstruct",
    "regenerated",
    "html",
    "raw-nltk",
    "camel",
]

_VALID_SEPS = {"_", "-", " ", ""}

_STYLE_HELP = """output style:
  plain                  readable POS annotations (default): n_Friends, v_come
  parse-tree             debug tabular view: segment, type, POS tag, abbreviation
  original-text          cat passthrough — output input unchanged, no parsing
  parse-and-reconstruct  reconstruct text from parse tree; == original-text iff lossless
  regenerated            alias for parse-and-reconstruct (backward compat)
  html                   full HTML page with 4 interactive view modes
  raw-nltk               raw NLTK Penn Treebank tags: NNS_Friends, VBP_come
  camel                  Hungarian Notation CamelCase: nFriends / friendsN (ignores SEP)"""

_POSITION_HELP = """annotation placement and separator:
  --prefix[=SEP]   annotation before word (default): n_Friends, n-Friends, nFriends
  --postfix[=SEP]  annotation after word:            Friends_n, Friends-n, Friendsn
  SEP choices: _  (default)  |  -  |  ' ' (space)  |  '' (empty, use --prefix= or --postfix=)
  Use = syntax for non-underscore separators: --prefix=-  --postfix=' '  --postfix=
  Styles that ignore position/SEP: parse-tree, original-text, parse-and-reconstruct"""


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pos-decorate",
        description="Decorate English text with Part-of-Speech annotations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input",
        nargs="?",
        metavar="FILE",
        help="input file (omit to read from stdin)",
    )
    parser.add_argument(
        "--style",
        choices=_STYLES,
        default="plain",
        metavar="STYLE",
        help=_STYLE_HELP,
    )

    pos_group = parser.add_mutually_exclusive_group()
    pos_group.add_argument(
        "--prefix",
        nargs="?",
        const="_",
        default=None,
        metavar="SEP",
        help="place annotation before word (default _); see position help below",
    )
    pos_group.add_argument(
        "--postfix",
        nargs="?",
        const="_",
        default=None,
        metavar="SEP",
        help="place annotation after word (default _); see position help below",
    )
    parser.add_argument(
        "--position-help",
        action="store_true",
        help="show detailed position/separator usage and exit",
    )
    parser.add_argument(
        "--verify-parse-and-regenerate",
        action="store_true",
        help=(
            "parse, regenerate, and diff against original; "
            "exit 0 if identical, exit 1 if not"
        ),
    )
    return parser


def _resolve_position(args: argparse.Namespace) -> tuple[str, str]:
    """Return (position, sep) from parsed args. Defaults to ('prefix', '_')."""
    if args.postfix is not None:
        return "postfix", args.postfix
    if args.prefix is not None:
        return "prefix", args.prefix
    return "prefix", "_"


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.position_help:
        print(_POSITION_HELP)
        sys.exit(0)

    position, sep = _resolve_position(args)

    if sep not in _VALID_SEPS:
        parser.error(
            f"invalid separator {sep!r} — must be one of: _ - (space) (empty string)"
        )

    if args.input:
        with open(args.input, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    # original-text needs no parsing — pure passthrough
    if args.style == "original-text":
        sys.stdout.write(fmt.original_text(text))
        return

    tokens = tokenize(text)

    if args.verify_parse_and_regenerate:
        is_clean, diff = fmt.verify_round_trip(text, tokens)
        if is_clean:
            print("OK — regenerated text is identical to original.")
            sys.exit(0)
        else:
            print("FAIL — regenerated text differs from original:")
            print(diff, end="")
            sys.exit(1)

    style = args.style
    dispatch = {
        "plain":                 lambda t: fmt.plain(t, position=position, sep=sep),
        "parse-tree":            fmt.parse_tree,
        "parse-and-reconstruct": fmt.parse_and_reconstruct,
        "regenerated":           fmt.regenerated,
        "html":                  lambda t: fmt.html(t, position=position, sep=sep),
        "raw-nltk":              lambda t: fmt.raw_nltk(t, position=position, sep=sep),
        "camel":                 lambda t: fmt.camel(t, position=position),
    }
    sys.stdout.write(dispatch[style](tokens))


if __name__ == "__main__":
    main()
