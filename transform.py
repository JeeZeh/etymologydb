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
apoc_file = Path("plugins") / Path("apoc.jar")
etymwn_file = Path("import") / Path("etymwn.tsv")
words_file = Path("import") / Path("words.csv")
relationships_file = Path("import") / Path("relationships.csv")


def strip_word(w: str):
    return (
        w.strip()
        .replace(r"(''|\[\[|\]\]|\"|\|)", "")
        .replace("[[", "")
        .replace("]]", "")
        .replace('"', "")
        .replace("|", "")
    )


def transform():
    ignore_edges = set(("has_derived_form", "etymology"))
    words: set[str] = set()

    print(f"Reading etymwn.csv and writing {words_file}")
    source = etymwn_file.open("r", encoding="utf8")
    target_relationships = relationships_file.open("w+", encoding="utf8")

    # target_relationships.write(relationships_header + "\n")
    for line in tqdm(csv.reader(source, delimiter="\t"), unit="lines"):
        w1, w2 = strip_word(line[0]), strip_word(line[2])
        words.add(w1)
        words.add(w2)
        if line[1][4:] not in ignore_edges:
            target_relationships.write(f"{w1}{delim}{line[1][4:]}{delim}{w2}\n")

    print(f"Writing {words_file}")
    target_words = words_file.open("w+", encoding="utf8")
    # target_words.write(words_header + "\n")
    for w in tqdm(words, unit="words"):
        target_words.write(f"{w}{delim}{w.replace(': ', delim, 1)}{delim}Word\n")

def download_etymwn():
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

def download_apoc():
    apoc_url = "https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.2.0.10/apoc-4.2.0.10-all.jar"
    print(f"Downloading {apoc_url} and extracting to {apoc_file}")

    # Download Etymwn
    r = requests.get(
        apoc_url,
        stream=True,
    )
    apoc_out = apoc_file.open("wb+")
    for chunk in r:
        apoc_out.write(chunk)


if __name__ == "__main__":
    download_apoc()
    download_etymwn()
    transform()

# type	amount
# "is_derived_from"	2267203
# "has_derived_form"	2267190
# "etymologically_related"	539761
# "etymological_origin_of"	477099
# "etymology"	474660
# "variant:orthography"	16561
# "derived"	2
# "etymologically"	1
