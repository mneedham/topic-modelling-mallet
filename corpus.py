import nltk
import csv
from collections import defaultdict

episodes = defaultdict(list)
with open("sentences.csv", "r") as file:
    reader = csv.reader(file, delimiter = ",")
    print reader.next()

    for row in reader:
        episodes[row[1]].append(row[4])

for episode, text in episodes.iteritems():
    with open("mallet-2.0.7/sample-data/himym/{0}.txt".format(episode), "w") as file:
        file.write(" ".join(text))
