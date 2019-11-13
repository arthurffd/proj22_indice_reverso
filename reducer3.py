#! /usr/bin/python3

# Python 3 Reducer script, for MapReduce jobs called by Hadoop Streaming jar
from sys import stdin
import re

# index dicitionary
index = {}

for line in stdin:
        # split word and docs postings (separated by tab)
        word, postings = line.split('\t')

        index.setdefault(word, {})
        
        for posting in postings.split(','):
                doc_id, count = posting.split(':')
                count = int(count)
                # sums word count for each document
                index[word].setdefault(doc_id, 0)
                index[word][doc_id] += count

# create the dictionary: word [doc_id: count, doc_id: count]
# example: someword [doc001: 5, doc002: 27, doc004: 2]
for word in index:
        postings_list = ["%s:%d" % (doc_id, index[word][doc_id])
                         for doc_id in index[word]]

        postings = ','.join(postings_list)
        print('%s\t%s' % (word, postings))

