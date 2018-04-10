#!/usr/bin/python3
## Summarises articles into n sentences

import nltk

with open('/tmp/para.txt', 'r') as f:
    text = f.read()
    f.close()

# Remove stop-words
stop_words = set(nltk.corpus.stopwords.words("english"))  # create a set of stop words
words = nltk.tokenize.word_tokenize(text)  # turn text into set of tokens
# Count number and frequency of non stop-words in text
word_freq = dict()
for word in words:
    word = word.lower()
    word = nltk.stem.PorterStemmer().stem(word)  # stems similar words (mom, mommy, mother etc) as one word
    if word in stop_words:
        continue
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

# Rank sentences by how many popular words they have
sentences = nltk.tokenize.sent_tokenize(text)  # turn text into token sentences
sentence_value = dict()
# Add frequency of every word in sentence to create a sentence score
for sentence in sentences:
    for word_key in word_freq:
        if word_key in sentence.lower():
            if sentence in sentence_value:
                sentence_value[sentence] += word_freq[word_key]
            else:
                sentence_value[sentence] = word_freq[word_key]
# Account for longer sentences having an advantage by dividing it by sentence length
sum_value = 0
sum_value_list = []
for sentence in sentence_value:
    sum_value += sentence_value[sentence]
    sum_value_list.append(sentence_value[sentence])
avg_sentence_value = int(sum_value/len(sentence_value))  # avg value of each sentence in original text

number_of_sentances_to_keep = 5
nth_number_interesting_score = sorted(sum_value_list, reverse=True)[number_of_sentances_to_keep]
summary_text = ''
for sentence in sentences:
    if sentence_value[sentence] > (nth_number_interesting_score):
        summary_text += " " + sentence

with open('/tmp/para_summarise.txt', 'a') as f:
    f.write(summary_text)
    f.close()
