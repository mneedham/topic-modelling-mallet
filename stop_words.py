import csv
import operator
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict

episodes = defaultdict(str)
with open("sentences.csv", "r") as file:
    reader = csv.reader(file, delimiter = ",")
    reader.next()
    for row in reader:
        episodes[row[1]] += row[4]

vectorizer = CountVectorizer(analyzer='word', min_df = 0, stop_words = 'english')
matrix = vectorizer.fit_transform(episodes.values())
features = vectorizer.get_feature_names()

words = {}
for doc_id, doc in enumerate(matrix.todense()):
    for word_id, score in enumerate(doc.tolist()[0]):
        word = features[word_id]
        if not words.get(word):
            words[word] = {}

        if not words[word].get("score"):
            words[word]["score"] = 0
        words[word]["score"] += score

        if not words[word].get("episodes"):
            words[word]["episodes"] = set()

        if score > 0:
            words[word]["episodes"].add(doc_id)

sorted_words = sorted(list(words.iteritems()), key = lambda x: -1 * len(x[1]["episodes"]))

with open("stop_words.txt", "w") as file:
    writer = csv.writer(file, delimiter = ",")
    for word, value in sorted_words:
        # appears in > 10% of episodes
        if len(value["episodes"]) > int(len(episodes) / 10):
            writer.writerow([word.encode('utf-8')])

        # less than 10 occurences
        if value["score"] < 10:
            writer.writerow([word.encode('utf-8')])
