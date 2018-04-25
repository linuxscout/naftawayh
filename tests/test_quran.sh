#!/bin/sh
#make date for output file
DATE=`date +%Y-%m-%d-%H:%M`

python -m cProfile test_wordtag_quran.py -f samples/quran_word_v0.6tag.csv >output/qurantag-${DATE}.txt

