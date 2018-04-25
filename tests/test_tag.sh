#!/bin/sh
DATE=`date +%Y-%m-%d-%H:%M`
python -m cProfile test_wordtag_file.py >output/wordtag-${DATE}.txt
