#!/bin/sh


train_model() {
  ./mallet-2.0.7/bin/mallet import-dir \
    --input mallet-2.0.7/sample-data/himym \
    --output ${2} \
    --keep-sequence \
    --remove-stopwords \
    --extra-stopwords ${1}
}

extract_topics() {
  ./mallet-2.0.7/bin/mallet train-topics \
    --input ${2} --num-topics ${1} \
    --optimize-interval 20 \
    --output-state himym-topic-state.gz \
    --output-topic-keys output/himym_${1}_${3}_keys.txt \
    --output-doc-topics output/himym_${1}_${3}_composition.txt
}

train_model "stop_words.txt" "output/himym.mallet"
train_model "main-words-stop.txt" "output/himym.main.words.stop.mallet"

extract_topics 10 "output/himym.mallet" "all.stop.words"
extract_topics 15 "output/himym.mallet" "all.stop.words"
extract_topics 20 "output/himym.mallet" "all.stop.words"
extract_topics 30 "output/himym.mallet" "all.stop.words"

extract_topics 10 "output/himym.main.words.stop.mallet" "main.stop.words"
extract_topics 15 "output/himym.main.words.stop.mallet" "main.stop.words"
extract_topics 20 "output/himym.main.words.stop.mallet" "main.stop.words"
extract_topics 30 "output/himym.main.words.stop.mallet" "main.stop.words"
