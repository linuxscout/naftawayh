#!/usr/bin/python
# -*- coding = utf-8 -*-
import sys
sys.path.append('../');
import naftawayh.wordtag 

word_list=(
     u'بالبلاد',
     u'بينما',
     u'أو',
     u'انسحاب',
     u'انعدام',
     u'انفجار',
     u'البرنامج',
     u'بانفعالاتها',
     u'العربي',
     u'الصرفي',
     u'التطرف',
     u'اقتصادي',
     )

tagger = naftawayh.wordtag.WordTagger();
#test word by word
print (" **** test word by word ***")
for word in word_list:
    if tagger.is_noun(word):
        print(u'%s is noun'%word)
    if tagger.is_verb(word):
        print(u'%s is verb'%word)
    if tagger.is_stopword(word):
        print(u'%s is stopword'%word)
previous_word=""
print (" **** test words in context***")
# test words in context
for word in word_list:
    tag=tagger.context_analyse(previous_word,word);
    print(u"%s from context is %s "%(word,tag))
    previous_word=word;
print (" **** test all words ***")
# test all words
list_tags = tagger.word_tagging(word_list)
for word, tag in zip(word_list, list_tags):
    print word, tag
