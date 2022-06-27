from collections import defaultdict
import csv
from zipfile import ZipFile
import requests
from tqdm import tqdm
from zipfile import ZipFile
import requests
import io

delim = "|"

def strip_word(w: str):
    return w.strip().replace(r"(''|\[\[|\]\]|\"|\|)", "").replace("[[", "").replace("]]", "").replace("\"", "").replace("|", "")


def transform():
    words_header = f"id:ID{delim}lang{delim}text{delim}:LABEL"
    relationships_header = f":START_ID{delim}:TYPE{delim}:END_ID"

    words: set[str] = set()

    print("Reading etymwn.csv and writing relationships.csv")
    with open("import/relationships.csv", mode="w+", encoding="utf8") as target_relationships:
        target_relationships.write(relationships_header + "\n")
        with open("import/etymwn.tsv", encoding="utf8") as source:
            for line in tqdm(csv.reader(source, delimiter="\t"), unit="lines"):
                w1, w2 = strip_word(line[0]), strip_word(line[2])
                words.add(w1)
                words.add(w2)
                target_relationships.write(f"{w1}{delim}{line[1][4:]}{delim}{w2}\n")

    print("Writing words.csv")
    with open("import/words.csv", mode="w+", encoding="utf8") as target_words:
        target_words.write(words_header + "\n")
        for w in tqdm(words, unit="words"):
            target_words.write(f"{w}{delim}{w.replace(': ', delim, 1)}{delim}Word\n")


# rm -rf /data/databases/neo4j
# neo4j-admin import --database neo4j --nodes "/import/words.csv" --relationships "/import/relationships.csv" --delimiter="|"


def download_etymwn():
    etymwn_url = "http://etym.org/etymwn-20130208.zip"
    print("Downloading", etymwn_url, "and extracting to import/")

    # Download Etymwn
    r = requests.get(
        etymwn_url,
        stream=True,
    )
    zip_as_bytes_io = io.BytesIO(r.content)
    zip_file = ZipFile(zip_as_bytes_io)
    zip_file.extractall("import/")


if __name__ == "__main__":
    download_etymwn()
    transform()
