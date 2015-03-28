import csv
import itertools
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import pylab
import matplotlib.pyplot as plt
pylab.show()

variations = [
    {"topics": 10, "stop_words": "all.stop.words"},
    {"topics": 10, "stop_words": "main.stop.words"},
    {"topics": 15, "stop_words": "all.stop.words"},
    {"topics": 15, "stop_words": "main.stop.words"},
    {"topics": 20, "stop_words": "all.stop.words"},
    {"topics": 20, "stop_words": "main.stop.words"},
    {"topics": 30, "stop_words": "all.stop.words"},
    {"topics": 30, "stop_words": "main.stop.words"}
]

for count,variation in enumerate(variations):
    count = count+1
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


    flattened_episodes = [{
                            "NumberInSeason": episode["NumberInSeason"],
                            "Title": episode["Title"],
                            "TopicId": topic["topic"],
                            "TopicScore": topic["score"]
                          }
                          for episode in episodes.values()
                          for topic in episode["Topics"]]

    df = pd.DataFrame(flattened_episodes)
    topics = df.groupby(["TopicId"]).size()
    ordered_topics = sorted(topics.iteritems(), key = lambda x: int(x[0]))
    print len(ordered_topics)

    ax = plt.subplot(4,2,count)
    width = 0.35

    x = [int(x[0]) for x in ordered_topics]

    ind = np.arange(len(x))
    ax.bar(ind + (width / 2), [x[1] for x in ordered_topics], width, color='blue')
    plt.xticks(ind + width, [int(x[0]) for x in ordered_topics])
    ax.set_xticklabels(ind, rotation=45)
    plt.xlabel('Topic Number')
    plt.ylabel('# of documents')

    left  = 0.125  # the left side of the subplots of the figure
    right = 0.9    # the right side of the subplots of the figure
    bottom = 0.1   # the bottom of the subplots of the figure
    top = 0.9      # the top of the subplots of the figure
    wspace = 0.2   # the amount of width reserved for blank space between subplots
    hspace = 0.5   # the amount of height reserved for white space between subplots
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)


plt.show()
