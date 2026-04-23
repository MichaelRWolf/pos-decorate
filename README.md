# pos-decorate

A command-line tool that ingests plain English text and outputs it decorated with
Part-of-Speech (POS) annotations in multiple styles.

## Usage

```bash
pos-decorate input.txt                      # plain POS prefixes (default)
pos-decorate input.txt --style=html > out.html
echo "Friends, Romans, countrymen" | pos-decorate
```

## Styles

| Style                        | Flag                            | Example                      |
| ---------------------------- | ------------------------------- | ---------------------------- |
| Plain POS prefixes (default) | `--style=plain`                 | `n_Friends, v_come, prep_to` |
| Full HTML with 4 view modes  | `--style=html`                  | See below                    |
| Debug parse tree             | `--style=parse-tree`            | tabular: segment, type, tag  |
| Raw NLTK Penn Treebank tags  | `--style=raw-nltk`              | `NNS_Friends, VBP_come`      |
| Hungarian Notation CamelCase | `--style=camel`                 | `nFriends, vCome`            |
| Passthrough (cat)            | `--style=original-text`         | unchanged input              |
| Round-trip reconstruction    | `--style=parse-and-reconstruct` | should equal original        |

## HTML View Modes

When `--style=html`, the output supports four interactive views toggled by buttons:

1. **As Written** — plain prose, no annotation (default)
2. **POS-Tagged** — POS prefix annotations as black/white text
3. **Tag-Receding** — annotations dimmed, words full black
4. **Grammar-Lit** — words color-coded by POS class, no tags

## Running Tests

```bash
source venv/bin/activate
pytest
```

Three approval tests verify parse tree output and tokenizer round-trip fidelity.

## Installation

```bash
git clone https://github.com/MichaelRWolf/pos-decorate.git
cd pos-decorate
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Prior Art

Earlier explorations of this idea, preserved unchanged for reference:

- [m_and_m_hungarian](https://github.com/MichaelRWolf/m_and_m_hungarian) — Python/NLTK decorator with approval tests (most complete, 25 commits)
- [NLTK-Hungarian](https://github.com/MichaelRWolf/NLTK-Hungarian) — minimal NLTK POS tagging proof-of-concept
- [Text-Format-Hungarian](https://github.com/MichaelRWolf/Text-Format-Hungarian) — Perl attempt; contains early research notes on HN history
- [PyEnglishHungarian](https://github.com/MichaelRWolf/PyEnglishHungarian) — PyCharm skeleton
- [PyHungarianNotation](https://github.com/MichaelRWolf/PyHungarianNotation) — empty skeleton
- [hungarian_decorator](https://github.com/MichaelRWolf/hungarian_decorator) — empty skeleton

## License

MIT
