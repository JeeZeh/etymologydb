from collections import defaultdict
import csv

words: set[str] = set()
with open("etymwn.csv", encoding="utf8") as source:
    for line in csv.DictReader(source):
        words.add(line["n1"])
        words.add(line["n2"].strip())
            
with open("words.csv", mode="w+", encoding="utf8") as target_words:
    for w in words:
        target_words.write(w)
        target_words.write(",")
        target_words.write(w.replace(": ", ",", 1))
        target_words.write(",")
        target_words.write("Word")
        target_words.write("\n")

# neo4j-admin import --database neo4j --nodes "words-header.csv,words.csv" --relationships "relationships-header.csv,etymwn.csv"