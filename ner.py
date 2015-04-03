import nltk
from nltk.tag.stanford import NERTagger
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

sys.stdout = open("named_entities.txt", "w")

def extract_entities(text):
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() == "PERSON":
                    print ' '.join(c[0] for c in chunk)
                    sys.stdout.flush()

def extract_entity_names(t):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
    return entity_names

if __name__ == "__main__":
    episode_id = sys.argv[1:][0]

    if episode_id == "all":
        episode_ids = range(1,209)
        for episode_id in episode_ids:
            with open("mallet-2.0.7/sample-data/himym/{0}.txt".format(episode_id)) as file:
                sentence = file.read().decode("utf-8")
            print extract_entities(sentence)
    else:
        with open("mallet-2.0.7/sample-data/himym/{0}.txt".format(episode_id)) as file:
            sentence = file.read().decode("utf-8")
        print extract_entities(sentence)

    # tokens = nltk.word_tokenize(sentence)
    # pos_tags = nltk.pos_tag(tokens)
    # chunked_sentences =  nltk.ne_chunk(pos_tags, binary=True)
    #
    # entity_names = []
    # for tree in chunked_sentences:
    #     named_entities = extract_entity_names(tree)
    #     entity_names.extend(named_entities)
    #
    # print set(entity_names)


# st = NERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
# for sent in nltk.sent_tokenize(text):
#     tokens = nltk.tokenize.word_tokenize(sent)
#     tags = st.tag(tokens)
#     for tag in tags:
#         if tag[1]=='PERSON': print tag
