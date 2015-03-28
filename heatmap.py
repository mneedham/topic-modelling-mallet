import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv

variations = [
    {"topics": 10, "stop_words": "all.stop.words"},
    # {"topics": 10, "stop_words": "main.stop.words"},
    {"topics": 15, "stop_words": "all.stop.words"},
    # {"topics": 15, "stop_words": "main.stop.words"},
    {"topics": 20, "stop_words": "all.stop.words"},
    # {"topics": 20, "stop_words": "main.stop.words"},
    {"topics": 30, "stop_words": "all.stop.words"}
    # {"topics": 30, "stop_words": "main.stop.words"}
]

for count,variation in enumerate(variations):
    print variation
    count = count+1

    episodes = {}
    with open("episodes_full.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            episodes[row["NumberOverall"]] = row

    with open("output/himym_{0}_{1}_keys.txt".format(variation["topics"], variation["stop_words"]), "r") as keys:
    # with open("output/himym_30_all.stop.words_keys.txt", "r") as keys:
        keys_reader = csv.reader(keys, delimiter = "\t")
        for row in keys_reader:
            print row

    with open("output/himym_{0}_{1}_composition.txt".format(variation["topics"], variation["stop_words"]), "r") as file:
    # with open("output/himym_30_all.stop.words_composition.txt") as file:
        reader = csv.reader(file, delimiter = "\t")
        reader.next()

        for row in reader:
            episode_id = row[1].split("/")[-1].split(".")[0]
            if not episodes[episode_id].get("Topics"):
                episodes[episode_id]["Topics"] = []
            for topic_id, score in [(pair[0], pair[1]) for pair in zip(row[2:][0::2],row[2:][1::2])]:
                episodes[episode_id]["Topics"].append({"topic": topic_id, "score": score})

    number_of_columns = len(episodes.items()[0][1]["Topics"])
    number_of_rows = len(episodes.items())

    rows = []
    for entry in episodes.items():
        row = np.zeros(number_of_columns)
        # row = [0] * number_of_columns
        episode_id = entry[0]
        value = entry[1]
        for x in value["Topics"]:
            row[int(x["topic"])] = float(x["score"])
        rows.append(row)

    data = np.array(rows)
    row_labels = range(0, number_of_columns)
    column_labels = range(0, number_of_rows)

    fig, ax = plt.subplots()

    # heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
    heatmap = ax.pcolormesh(data, cmap=plt.cm.Blues)
    # p = ax.pcolormesh(np.random.randn(10,10))

    ax.axis([0, number_of_columns, 0, number_of_rows])
    ax.set_xticks(np.array(range(0,number_of_columns))+0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.set_xticklabels(row_labels, minor=False)


    plt.savefig('{0}_{1}.png'.format(variation["topics"], variation["stop_words"]), bbox_inches='tight')
    # plt.show()
