import csv
import itertools
import pandas as pd

variations = [
    {"topics": 10, "stop_words": "all.stop.words"},
    {"topics": 15, "stop_words": "all.stop.words"},
    {"topics": 20, "stop_words": "all.stop.words"},
    {"topics": 30, "stop_words": "all.stop.words"},
    {"topics": 10, "stop_words": "main.stop.words"},
    {"topics": 15, "stop_words": "main.stop.words"},
    {"topics": 20, "stop_words": "main.stop.words"},
    {"topics": 30, "stop_words": "main.stop.words"}
]

for variation in variations:
    episodes = {}
    with open("episodes_full.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            episodes[row["NumberOverall"]] = row

    print variation
    topics = {}
    with open("output/himym_{0}_{1}_keys.txt".format(variation["topics"], variation["stop_words"]), "r") as keys, \
         open("output/himym_{0}_{1}_composition.txt".format(variation["topics"], variation["stop_words"]), "r") as comp:
        keys_reader = csv.reader(keys, delimiter = "\t")
        for row in keys_reader:
            topics[row[0]] = {"importance": float(row[1]), "words": row[2]}

        for topic in sorted(topics.iteritems(), key=lambda x: int(x[0])):
            print topic

        comp_reader = csv.reader(comp, delimiter = "\t")
        comp_reader.next()
        for row in comp_reader:
            episode_id = row[1].split("/")[-1].split(".")[0]
            if not episodes[episode_id].get("Topics"):
                episodes[episode_id]["Topics"] = []
            for topic_id, score in [(pair[0], pair[1]) for pair in zip(row[2:][0::2],row[2:][1::2]) if float(pair[1]) > 0.20]:
                episodes[episode_id]["Topics"].append({"topic": topic_id, "score": score})


    flattened_episodes = [{ "NumberInSeason": episode["NumberInSeason"],
                            "Title": episode["Title"],
                            "TopicId": topic["topic"],
                            "TopicScore": topic["score"]
                          }
                          for episode in episodes.values()
                          for topic in episode["Topics"]]

    df = pd.DataFrame(flattened_episodes)
    print df.groupby(["TopicId"]).size().order(ascending = False)
