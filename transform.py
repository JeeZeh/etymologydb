from collections import defaultdict
import csv
from pathlib import Path
from zipfile import ZipFile
import requests
from tqdm import tqdm
from zipfile import ZipFile
import requests
import io

delim = "|"
root = Path("import")
root.mkdir(exist_ok=True)
etymwn_file = Path("import") / Path("etymwn.tsv")
words_file = Path("import") / Path("words.csv")
guidance_file = Path("import") / Path("README.md")


def strip_word(w: str):
    return (
        w.strip()
        .replace("''", "")
        .replace("[[", "")
        .replace("]]", "")
        .replace('"', "")
        .replace("|", "")
    )


def fix_relation(rel: str):
    rel = rel.strip().replace(":", "_")

    if rel == "derived":
        return "is_derived_from"
    if rel == "etymologically":
        return "etymologically_related"

    return rel


def word_load_script(word_files: list[str]):
    lines = []
    for file in word_files:
        lines.append(
            f"""
LOAD CSV FROM "/import/{file}" NO HEADER DELIMITER "|" AS line
CREATE (w:Word {{ id: line[0], lang: line[1], name: line[2] }})
RETURN COUNT(w) AS `Inserted`;
"""
        )

    return "\n".join(lines)


def edge_load_script(edge_files: list[str]):
    lines = []
    for file in edge_files:
        rel = file.split(".csv")[0]
        lines.append(
            f"""
LOAD CSV FROM "/import/{file}" NO HEADER DELIMITER "|" AS line
MATCH (a:Word {{ id: line[0] }}), (b:Word {{ id: line[2] }})
CREATE (a)-[r:{rel}]->(b)
RETURN COUNT(r) AS `Inserted {rel}`;"""
        )

    return "\n".join(lines)


def print_guidance(word_files, edge_files):
    return f"""
## Preperation

```cypherl
// Clear data
MATCH (n)
DELETE n;
```

Then

```cypherl
STORAGE MODE IN_MEMORY_ANALYTICAL;
```

Load words
```
{word_load_script(word_files)}
```

Create indexes
```
CREATE INDEX ON :Word(id);
CREATE INDEX ON :Word(label);
CREATE INDEX ON :Word(name);
```

Load edges
```
{edge_load_script(edge_files)}
```
Example query

```
MATCH (w:Word {{name: "television"}})
RETURN w;
```
"""


def transform():
    word_files = []
    edge_files = []
    redundant_pairs = {
        "has_derived_form": "is_derived_from",
        "etymology": "etymological_origin_of",
        "etymologically_related": "etymologically_related",
    }
    words: set[str] = set()
    rels: set[tuple[str, str, str]] = set()

    print(f"Reading etymwn.csv")
    source = etymwn_file.open("r", encoding="utf8")

    # target_relationships.write(relationships_header + "\n")
    for line in tqdm(csv.reader(source, delimiter="\t"), unit="lines"):
        w1, w2 = strip_word(line[0]), strip_word(line[2])
        words.add(w1)
        words.add(w2)
        rel = fix_relation(line[1][4:])
        rels.add((w1, rel, w2))

    # TODO: Add is_suffix/is_prefix property
    print(f"Writing {words_file}")
    target_words = words_file.open("w+", encoding="utf8")
    # target_words.write(words_header + "\n")
    for w in tqdm(words, unit="words"):
        target_words.write(f"{w}{delim}{w.replace(': ', delim, 1)}{delim}Word\n")
    word_files.append(words_file.name)

    print(f"Filtering and processing relationships")
    rels_filtered = set()
    for r in tqdm(rels, unit="rels"):
        # Don't create edges in both directions
        if r[1] in redundant_pairs and (r[2], redundant_pairs[r[1]], r[0]) in rels:
            continue

        rels_filtered.add(r)

    by_relationship = defaultdict(list)
    for w1, r, w2 in rels_filtered:
        by_relationship[r].append((w1, w2))

    for r, pairs in by_relationship.items():
        relationships_file = Path("import") / Path(f"{r}.csv")
        edge_files.append(relationships_file.name)
        print(f"Writing {relationships_file}")
        out_file = relationships_file.open("w+", encoding="utf-8")
        for w1, w2 in tqdm(pairs, unit="rels"):
            out_file.write(f"{w1}{delim}{r}{delim}{w2}\n")

    guidance_file.open("w+").write(print_guidance(word_files, edge_files))


def download_etymwn():
    if etymwn_file.exists():
        print(f"{etymwn_file} already exists, skipping download.")

        return
    etymwn_url = "http://etym.org/etymwn-20130208.zip"
    print(f"Downloading {etymwn_url} and extracting to {etymwn_file.parent.absolute()}")

    # Download Etymwn
    r = requests.get(
        etymwn_url,
        stream=True,
    )
    zip_as_bytes_io = io.BytesIO(r.content)
    zip_file = ZipFile(zip_as_bytes_io)
    zip_file.extractall(etymwn_file.parent)


if __name__ == "__main__":
    download_etymwn()
    transform()
