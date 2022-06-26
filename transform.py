from collections import defaultdict
import csv
from zipfile import ZipFile
import requests
from tqdm import tqdm

words_header = "id:ID,lang,text,:LABEL"
relationships_header = ":START_ID,:TYPE,:END_ID"

words: set[str] = set()
relation: list[str] = []

print("Reading etymwn.csv")
with open("import/etymwn.tsv", encoding="utf8") as source:
    for line in tqdm(csv.reader(source, delimiter="\t"), unit="lines"):
        words.add(line[0])
        words.add(line[2].strip())
        relations.append(",".join((line[0], line[1].split(":")[1], line[2])))

print("Writing relationships.csv")
with open("import/relationships.csv", mode="w+", encoding="utf8") as target_relationships:
    target_relationships.write(relationships_header + "\n")
    for relationship in tqdm(relations, unit="rels"):
        target_relationships.write(relationship)
        target_relationships.write("\n")

print("Writing words.csv")
with open("import/words.csv", mode="w+", encoding="utf8") as target_words:
    target_words.write(words_header + "\n")
    for w in tqdm(words, unit="words"):
        target_words.write(",".join((w, w.replace(": ", ",", 1), "Word")))
        target_words.write("\n")

# neo4j-admin import --database neo4j --nodes "words-header.csv,words.csv" --relationships "relationships-header.csv,etymwn.csv"
