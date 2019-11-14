#! /usr/bin/python3

# Python 3 Reducer script, for MapReduce jobs called by Hadoop Streaming jar

# DICTIONARY Word Index reference
# Expected Output: <word> /t <word_id>
# Example: someword  1 ,  anotherword  2,   anything 3,   hamlet 4

from sys import stdin
import re

index = {}
dicn = {}


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
        dicn[word] = i
        print('{}\t{}'.format(word, i))
        i += 1


