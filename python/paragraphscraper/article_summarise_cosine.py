#!/usr/bin/env python
"""Edited version of
https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70
"""

import click
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

def read_article(file_name):
    """ Generates clean sentences"""
    sentences = []
    with open(file_name, "r") as file:
        filedata = file.readlines()

    for entry in filedata:
        entry = entry.replace("[^a-zA-Z]", " ")
        entry = entry.replace("\n", "")
        entry_list = entry.split(". ")
        for item in entry_list:
            if not item.strip() == "":
                sentences.append(item.strip())

    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    """ Use Cosine similarity between two vectors to see how similar they are"""
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    """ Create an empty similarity matrix """
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

@click.command()
@click.option(
    "--file-name",
    type=click.Path(exists=True, readable=True, resolve_path=True),
    default="/tmp/para.txt",
    prompt=True,
    help="The text file you want to summarize",
    show_default=True,
)
@click.option(
    "--top-n",
    type=click.INT,
    help="How many sentences to summarize to",
    default=5,
    show_default=True,
)
@click.option(
    "--context",
    is_flag=True,
    help="Shows the sentence befroe and after the important one",
)
def generate_summary(file_name, top_n, context):
    """ Summarises file_name into 5 sentences """
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_article(file_name)
    #print(sentences)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)
    #print(sentence_similarity_martix)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    #print("Indexes of top ranked_sentence order are ", ranked_sentence)

    for i in range(top_n):
        sentence_index = sentences.index(ranked_sentence[i][1])
        #Pads number to 4 digits
        if context:
            summary_string = f'{sentence_index:04}: {sentences[sentence_index - 1]}. {sentences[sentence_index]}. {sentences[sentence_index + 1]}'
        else:
            summary_string = f'{sentence_index:04}: {sentences[sentence_index]}'
        summarize_text.append(summary_string)

    # Step 5 - Offcourse, output the summarize texr
    summarize_text.sort()
    #Now have the most important sentences, in the order they appeared
    final_list = []
    for i in summarize_text:
        final_summary = ""
        final_summary = final_summary.join(i.split(": ")[1])
        final_list.append(final_summary)
    print(f'Summary:\n{". ".join(final_list)}')
    #print(f'Summary:\n{final_summary}')

if __name__ == "__main__":
    generate_summary()
