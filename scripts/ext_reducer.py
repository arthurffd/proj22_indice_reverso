#! /usr/bin/python3

# Python 3 Reducer script, for MapReduce jobs called by Hadoop Streaming jar

# EXTENDED Reversed (Inverted) Index 

# Expected Output: <word> /t <[doc_id: count]
# Example: someword  [7: 1, 22: 5, 30: 20] ,  anotherword    [31: 3],  anything    [1: 1, 3: 1, 4: 5, 10: 3, 23: 10]

from sys import stdin
import re

index = {}

for line in stdin:
        word, postings = line.split('\t')

        index.setdefault(word, {})

        for posting in postings.split(','):
                doc_id, count = posting.split(':')
                count = int(count)

                index[word].setdefault(doc_id, 0)
                index[word][doc_id] += count

for word in sorted(index):
        postings_list = ["%s:%d" % (doc_id, index[word][doc_id])
                         for doc_id in index[word]]

        postings = ','.join(postings_list)
        print('%s\t%s' % (word, postings))

