#! /usr/bin/python3

# Python 3 Reducer script, for MapReduce jobs called by Hadoop Streaming jar

# REVERSED (Inverted) Index 

# Expected Output: <word_id> /t <[doc_id]
# Example: 1    [7, 22, 30] ,  2    [31],  3    [1, 3, 4, 10, 23]

from sys import stdin
import re
import os

index = {}
reverse = {}

for line in stdin:
        word, postings = line.split('\t')

        index.setdefault(word, {})

        for posting in postings.split(','):
                doc_id, count = posting.split(':')
                count = int(count)

                index[word].setdefault(doc_id, 0)
                index[word][doc_id] += count


i = 0
for word in sorted(index):
        reverse[i] = ['%s' % (doc_id) for doc_id in index[word]]
        print('{}\t{}'.format(i, reverse[i]))
        i += 1

