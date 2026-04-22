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

_STYLE_HELP = """output style:
  plain                  readable POS prefix annotations (default): n_Friends, v_come
  parse-tree             debug tabular view: segment, type, POS tag, abbreviation
  original-text          cat passthrough — output input unchanged, no parsing
  parse-and-reconstruct  reconstruct text from parse tree; == original-text iff lossless
  regenerated            alias for parse-and-reconstruct (backward compat)
  html                   full HTML page with 4 interactive view modes
  raw-nltk               raw NLTK Penn Treebank tags: NNS_Friends, VBP_come
  camel                  Hungarian Notation CamelCase: nFriends, vCome"""


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
    parser.add_argument(
        "--verify-parse-and-regenerate",
        action="store_true",
        help=(
            "parse, regenerate, and diff against original; "
            "exit 0 if identical, exit 1 if not"
        ),
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

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
        "plain":                 fmt.plain,
        "parse-tree":            fmt.parse_tree,
        "parse-and-reconstruct": fmt.parse_and_reconstruct,
        "regenerated":           fmt.regenerated,
        "html":                  fmt.html,
        "raw-nltk":              fmt.raw_nltk,
        "camel":                 fmt.camel,
    }
    sys.stdout.write(dispatch[style](tokens))


if __name__ == "__main__":
    main()
