#!/usr/bin/python3
## Summarises articles into n sentances

import nltk

with open('/tmp/para.txt', 'r') as f:
    text = f.read()
    f.close()

#Remove stop-words
stop_words = set(nltk.corpus.stopwords.words("english")) #create a set of stop words
words = nltk.tokenize.word_tokenize(text) #turn text into set of tokens
#Count number and frequency of non stop-words in text
word_freq = dict()
for word in words:
    word = word.lower()
    word = nltk.stem.PorterStemmer().stem(word) #stems similar words (mom, mommy, mother etc) as one word
    if word in stop_words:
        continue
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

#Rank sentances by how many popular words they have
sentances = nltk.tokenize.sent_tokenize(text) #turn text into token sentances
sentance_value = dict()
#Add frequency of every word in sentance to create a sentance score
for sentance in sentances:
    for word_key in word_freq:
        if word_key in sentance.lower():
            if sentance in sentance_value:
                sentance_value[sentance] += word_freq[word_key]
            else:
                sentance_value[sentance] = word_freq[word_key]
#Account for longer sentances having an advantage by dividing it by sentance length
sum_value = 0
for sentance in sentance_value:
    sum_value += sentance_value[sentance]
avg_sentance_value = int(sum_value/len(sentance_value)) #avg value of each sentance in original text

summary_text = ''
for sentance in sentances:
    if sentance_value[sentance] > (1.05 * avg_sentance_value):
        summary_text += " " + sentance

with open('/tmp/para_summarise.txt', 'a') as f:
    f.write(summary_text)
