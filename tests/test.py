#!/usr/bin/python
# -*- coding = utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
import unittest
import sys
sys.path.append('../naftawayh')
import naftawayh.wordtag
class NaftwayhTestCase(unittest.TestCase):
    """Tests for `Stopwords.py`."""

    def test_is_noun(self):
        """Test is_noun"""
        tagger = naftawayh.wordtag.WordTagger();        
        self.assertEqual(tagger.is_noun(u'بالبلاد'), True)
        self.assertEqual(tagger.is_noun(u'بينما'), True)
        self.assertEqual(tagger.is_noun(u'أو'), True)
        self.assertEqual(tagger.is_noun(u'انسحاب'), True)
        self.assertEqual(tagger.is_noun(u'انعدام'), True)
        self.assertEqual(tagger.is_noun(u'انفجار'), True)
        self.assertEqual(tagger.is_noun(u'البرنامج'), True)
        self.assertEqual(tagger.is_noun(u'بانفعالاتها'), True)
        self.assertEqual(tagger.is_noun(u'العربي'), True)
        self.assertEqual(tagger.is_noun(u'الصرفي'), True)
        self.assertEqual(tagger.is_noun(u'التطرف'), True)
        self.assertEqual(tagger.is_noun(u'اقتصادي'), True)
    
    def test_is_verb(self):
        """Test is_verb"""
        tagger = naftawayh.wordtag.WordTagger();        
        self.assertEqual(tagger.is_verb(u'بالبلاد'), False)
        self.assertEqual(tagger.is_verb(u'بينما'), True)
        self.assertEqual(tagger.is_verb(u'أو'), True)
        self.assertEqual(tagger.is_verb(u'انسحاب'), False)
        self.assertEqual(tagger.is_verb(u'انعدام'), False)
        self.assertEqual(tagger.is_verb(u'انفجار'), False)
        self.assertEqual(tagger.is_verb(u'البرنامج'), False)
        self.assertEqual(tagger.is_verb(u'بانفعالاتها'), False)
        self.assertEqual(tagger.is_verb(u'العربي'), False)
        self.assertEqual(tagger.is_verb(u'الصرفي'), False)
        self.assertEqual(tagger.is_verb(u'التطرف'), False)
        self.assertEqual(tagger.is_verb(u'اقتصادي'), False)

    def test_is_stopword(self):
        """Test is_stopword"""
        tagger = naftawayh.wordtag.WordTagger();
        self.assertEqual(tagger.is_stopword(u'بالبلاد'), False)
        self.assertEqual(tagger.is_stopword(u'بينما'), False)
        self.assertEqual(tagger.is_stopword(u'أو'), True)
        self.assertEqual(tagger.is_stopword(u'انسحاب'), False)
        self.assertEqual(tagger.is_stopword(u'انعدام'), False)
        self.assertEqual(tagger.is_stopword(u'انفجار'), False)
        self.assertEqual(tagger.is_stopword(u'البرنامج'), False)
        self.assertEqual(tagger.is_stopword(u'بانفعالاتها'), False)
        self.assertEqual(tagger.is_stopword(u'العربي'), False)
        self.assertEqual(tagger.is_stopword(u'الصرفي'), False)
        self.assertEqual(tagger.is_stopword(u'التطرف'), False)
        self.assertEqual(tagger.is_stopword(u'اقتصادي'), False)

    def test_is_context_analyse(self):
        """Test is_stopword"""      
        tagger = naftawayh.wordtag.WordTagger();  
        self.assertEqual(tagger.context_analyse(u'',u'بالبلاد'), u'vn')
        self.assertEqual(tagger.context_analyse(u'بالبلاد',u'بينما'), u'vn')
        self.assertEqual(tagger.context_analyse(u'بينما',u'أو'), u'vn')
        self.assertEqual(tagger.context_analyse(u'أو',u'انسحاب'), u'vn')
        self.assertEqual(tagger.context_analyse(u'انسحاب',u'انعدام'), u'vn')
        self.assertEqual(tagger.context_analyse(u'انعدام',u'انفجار'), u'vn')
        self.assertEqual(tagger.context_analyse(u'انفجار',u'البرنامج'), u'vn')
        self.assertEqual(tagger.context_analyse(u'البرنامج',u'بانفعالاتها'), u'vn')
        self.assertEqual(tagger.context_analyse(u'بانفعالاتها',u'العربي'), u'vn')
        self.assertEqual(tagger.context_analyse(u'العربي',u'الصرفي'), u'vn')
        self.assertEqual(tagger.context_analyse(u'الصرفي',u'التطرف'), u'vn')
        self.assertEqual(tagger.context_analyse(u'التطرف',u'اقتصادي'), u'vn')        
if __name__ == '__main__':
    unittest.main()

    
