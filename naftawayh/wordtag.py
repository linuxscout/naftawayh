#!/usr/bin/python
# -*- coding=utf-8 -*-
"""
Arabic Word Type Guessing:
This class can identify the typoe of word (noun, verb, prepostion).
"""
import tashaphyne
from stopwords import *
#
import re
import string
import sys
from arabic_const import *
from ar_ctype import *
##from pysqlite2 import dbapi2 as sqlite
from affix_const import *

class WordTagger():
    """
    Arabic Word type Guessing
    """
    def __init__(self,):
        self.word=u"";
        self.verbstemmer=tashaphyne.ArabicLightStemmer();
        # prepare the verb stemmer
    	verb_prefix=u"أسفلونيتا"
    	verb_infix=u"اتويدط"
    	verb_suffix=u"امتةكنهوي"
    	verb_max_prefix=4
    	verb_max_suffix=6
        self.verbstemmer.set_max_prefix_length(verb_max_prefix);
        self.verbstemmer.set_max_suffix_length(verb_max_suffix);
        self.verbstemmer.set_prefix_letters(verb_prefix);
        self.verbstemmer.set_suffix_letters(verb_suffix);
        self.verbstemmer.set_prefix_list(VERBAL_PREFIX_LIST);
        self.verbstemmer.infix_letters=verb_infix;
        # prepare the noun stemmer
        self.nounstemmer=tashaphyne.ArabicLightStemmer();
        noun_prefix=u"مأسفلونيتاكب"
    	noun_infix=u"اتويدط"
    	noun_suffix=u"امتةكنهوي"
    	noun_max_prefix=4
    	noun_max_suffix=6

        self.nounstemmer.set_max_prefix_length(noun_max_prefix);
        self.nounstemmer.set_max_suffix_length(noun_max_suffix);
        self.nounstemmer.set_prefix_letters(noun_prefix);
        self.nounstemmer.set_suffix_letters(noun_suffix);
        self.nounstemmer.set_prefix_list(NOMINAL_PREFIXES_LIST);
        self.nounstemmer.infix_letters=noun_infix;


    def is_noun(self,word):
        """
        Return True if the word is a possible noun form

        @param word: word.
        @type word: unicode.
        @return: is a noun or not
        @rtype: Boolean
        """
        if self.is_possible_noun(word)>0:
            return True;
        else:
            return False;

    def is_verb(self,word):
        """
        Return True if the word is a possible verb form

        @param word: word.
        @type word: unicode.
        @return: is a noun or not
        @rtype: Boolean
        """

        if self.is_possible_verb(word)>0:
            return True;
        else:
            return False;

    def is_possible_noun(self,word):
        """
        Return True if the word is a possible noun form
        This function return True, if the word is valid, else, return False

        @param word: word.
        @type word: unicode.
        @return: error code : indicate the id of the rules aplied. Negative, if not a verb
        @rtype: integer
        """

    	self.verbstemmer.lightStem(word);
    	starword=self.verbstemmer.get_starword();
    	word_nm=self.verbstemmer.get_unvocalized();
    	guessed_word=self.guess_stem(word_nm)
    # HAMZA BELOW ALEF
    	if re.search(ur"[%s%s%s%s%s]"%(ALEF_HAMZA_BELOW,TEH_MARBUTA,FATHATAN,DAMMATAN,KASRATAN),word):
             return 100;

    	elif re.search(ur"[%s](.)+"%ALEF_MAKSURA,word):
             return 120;
    # the word ends with wa  a is WAW alef , is a verb
    	if re.search(ur"([^%s%s%s]..)%s%s$"%(ALEF_HAMZA_ABOVE, WAW,FEH,WAW,ALEF),starword) :
    	    return -160;

    # the word is started by Noon, before REH or LAM, or Noon, is a verb and not a noun
    	if re.match(ur"^%s[%s%s%s]"%(NOON,REH,LAM,NOON),word_nm):

    		return -10;
    # the word is started by YEH,
    # before some letters is a verb and not a noun
    	if re.match(ur"^%s[%s%s%s%s%s%s%s%s%s%s%s%s%s]"%(YEH,THAL,JEEM,HAH,KHAH,ZAIN,SHEEN,SAD,DAD,TAH,ZAH,GHAIN,KAF,YEH),word_nm):

    		return -20;


    # the word is like inf3l pattern
    	if re.search(ur"[%s%s%s%s%s]\*%s\*\*"%(ALEF,YEH,NOON,TEH,ALEF_HAMZA_ABOVE,TEH),starword):

    		return -30;
    # the word is like ift3l pattern
    	if re.search(ur"[%s%s%s%s%s]%s\*\*\*"%(ALEF,YEH,NOON,TEH,ALEF_HAMZA_ABOVE,NOON),starword):

    		return -40;
    # the word is like isf3l pattern
    	if re.search(ur"[%s%s%s%s%s]%s%s([^%s%s%s]{2})([^%s%s%s%s])"%(ALEF,YEH,NOON,TEH,ALEF_HAMZA_ABOVE,SEEN,TEH,ALEF,YEH,WAW,ALEF,HEH,KAF,NOON),word_nm):

    		return -50;
    # the word contains y|t|A)st*
    # يست، أست، نست، تست
    	if re.search(ur"(%s|%s|%s|%s)%s%s\*"%(ALEF_HAMZA_ABOVE,YEH,TEH,NOON,SEEN,TEH),starword) :

    		return -60;
    # the word contains ist***
    # استفعل
    	if re.search(ur"%s%s%s\*\*\*"%(ALEF,SEEN,TEH),starword) :

    		return -70;

    # the word contains ***t when **+t+* t is TEH
    # if TEH is followed by meem, alef, noon
    # تم، تما، تن، تا، تني
    # حالة تنا غير مدرجة
    	if re.search(ur"\*\*\*%s(%s|%s|%s[^%s])"%(TEH,MEEM,ALEF,NOON,ALEF),starword) :

    		return -80;

    #To reDo
    ### case of ***w  w is waw, this case is a verb,
    ### the case of ***w* is a noun
    ##	if re.search(u"\*\*\*%s[^\*%s]"%(WAW,NOON),starword):
    ##		if starword.count("*")==3:
    ##
    ##		  return -90;
    ##		else:
    ##		  if re.search(u"\*\*\*\*%s%s"%(WAW,ALEF),starword):
    ##		    return -100;

    # case of future verb with waw noon,
    	if re.search(u"^([^\*%s])*[%s%s](.)*\*\*\*%s%s"%(MEEM,YEH,TEH,WAW,NOON),starword):
    	    return -110;
    # case of future verb with ALEf noon,
    	if re.search(u"^([^\*%s])*[%s%s](.)*\*\*\*%s%s"%(MEEM,YEH,TEH,ALEF,NOON),starword):
    	    return -115;

    # case of yt,tt,nt and 3 stars is a verb like yt*** or yt*a**
    # at is an ambiguous case with hamza of interogation.
    	if re.search(u"^([^\*])*[%s%s%s]%s(\*\*\*|\*%s\*\*)"%(YEH,TEH,NOON, TEH,ALEF),starword):
    	    return -120;
    # case of yn,tn,nn and 3 stars is a verb like yn*** or yn*a* or ynt**

    	if re.search(u"^([^\*])*[%s%s%s]%s(\*\*\*|\*%s\*|%s\*\*)"%(YEH,TEH,NOON,NOON,ALEF,TEH),starword):

    	    return -130;
    # case of y***, y
    # exception ; case of y**w*
    	if re.search(u"^([^\*])*%s(\*\*\*|\*%s\*\*)"%(YEH,ALEF),starword):

    	    return -140;
# To do
# لا تعمل مع كلمة البرنامج
##    # the word contains a****  a is alef is a verb
##    	if re.search(ur"^([^\*])*%s(\*\*\*\*)"%(ALEF),starword) :
##
##    	    return -150;

    # the word has suffix TM (TEH MEEM)  and two original letters at list, is a verb
    	if re.search(u"%s%s([^\*])*$"%(TEH,MEEM),starword) and starword.count("*")>=2 :

    	    return -170;
    # the word ends with an added TEH
    	if re.search(u"-%s$"%(TEH),guessed_word):
    	    return -180;
    # the word starts with  an added YEH
    	if re.search(u"^%s-"%(YEH),guessed_word):
    	    return -190;

    	return 100;

    #---------------------------------------
    def is_possible_verb(self,word):
        """
        Return True if the word is a possible verb form
        This function return True, if the word is valid, else, return False
        A word is not valid verb if :
          - minimal lenght : 3
          - starts with ALEF_MAKSURA, WAW_HAMZA,YEH_HAMZA,
            HARAKAT
          - contains : TEH_MARBUTA
          - contains  ALEF_MAKSURA at the began or middle.
          - contains : double haraka : a warning
          - contains : ALEF_HAMZA_BELOW
          - contains: tanween
        @param word: word.
        @type word: unicode.
        @return: error code : indicate the id of the rules aplied. Negative, if not a verb
        @rtype: integer


        """

    	self.nounstemmer.lightStem(word);
    	starword=self.nounstemmer.get_starword();
    	word_nm=self.nounstemmer.get_unvocalized();

    ##	word_nm=ar_strip_marks_keepshadda(word);
        # affixed starword, is a which we srip affix and not derived,
        # for example meem is not an affix, but is a deiveitional letter
        # تنزع السوابق الالتصاقية مثل بال، ولا تنزع السوابق الاشتقاقية مثل مست

##    	affixed_noun_prefix=u"أفلواكب"
##    	affixed_noun_infix=u"اتوي"
##    	affixed_noun_suffix=u"امتةكنهوي"
##    	affixed_noun_max_prefix=4
##    	affixed_noun_max_suffix=6
##    	affixed_starword,affixed_left,affixed_right=self.nounstemmer.transformToStars(word);

    	if re.search(ur"^[%s%s%s%s%s%s]"%(WAW_HAMZA,YEH_HAMZA,FATHA,DAMMA,SUKUN,KASRA),word):
             return -1000;

    # HAMZA BELOW ALEF
    	elif re.search(ur"[%s%s%s%s%s]"%(ALEF_HAMZA_BELOW,TEH_MARBUTA,FATHATAN,DAMMATAN,KASRATAN),word):
             return -1010;

    	elif re.search(ur"[%s](.)+"%ALEF_MAKSURA,word):
             return -1020;


    # the word is like ift3al pattern
    	elif re.match(ur"%s([^%s%s%s%s%s]%s|[%s%s%s]%s|[%s]%s)(.)%s([^%s%s%s])"%(ALEF,LAM,SEEN,SAD,DAD,ZAH,TEH,SAD,DAD,ZAH,TAH,ZAIN,DAL,ALEF,HEH,KAF,NOON),word_nm):
    	   return -1030;
    # the word is like inf3al pattern
    	elif re.match(ur"%s%s(..)%s([^%s%s%s])"%(ALEF,NOON,ALEF,HEH,KAF,NOON),word_nm):

    	   return -1040;

    # the word is like isf3al pattern
    	elif re.match(ur"%s%s%s(..)%s([^%s%s%s])"%(ALEF,SEEN,TEH,ALEF,HEH,KAF,NOON),word_nm):

    	   return -1050;

    # the word is finished by HAMZA preceded by ALEF
    #and more than 2 originals letters
    	elif re.match(ur"[^%s%s%s%s%s%s%s%s]{2,}%s%s(.)*"%(YEH,FEH,LAM,NOON,ALEF_HAMZA_ABOVE,TEH,WAW,ALEF,ALEF,HAMZA),word_nm):
    	   return -1060;

    # the word contains three ALEF,
    # the kast ALEF musn't be at end
    	if re.match(ur"^(.)*([%s](.)+){3}$"%(ALEF),word_nm):

    	   return -1070;

    # the word is started by beh, before BEH,FEH,MEEM
    #is a noun and not a verb
    	if re.match(ur"^%s[%s%s%s]"%(BEH,BEH,FEH,MEEM),word_nm):

    	   return -1080;

    # the word is started by meem, before BEH,FEH,MEEM
    #is a noun and not a verb
    	if re.match(ur"^%s[%s%s%s]"%(MEEM,BEH,FEH,MEEM),word_nm):

    	   return -1090;

    # the word is started  by ALEF LAM
    # and the  original letters are more than two,
    	if re.match(ur"^[%s|%s]?[%s|%s]?%s%s(.){3,8}"%(FEH,WAW,KAF,BEH,ALEF,LAM),word_nm) or re.match(ur"^[%s|%s]?%s%s(.){3,8}"%(FEH,WAW,LAM,LAM),word_nm):
    	   min=word_nm.find(ALEF+LAM);
    	   if min<0: min=word_nm.find(LAM+LAM);
    	   min+=2;
    	   if min<len(word_nm):
    	       suffixes=u"امتةكنهوي"
    	       infixes=u"اتوي";
    	       word_nm2=word_nm[min:]
    	       word_nm2=re.sub(u"[^%s]"%suffixes, '*',word_nm2)
    #the meem is suffixes if is preceded by Heh or Kaf
    	       word_nm2=re.sub(u"(?<!(%s|%s|%s))%s"%(KAF,HEH,TEH,MEEM), '*',word_nm2)
    	       max=word_nm2.rfind('*');
    	       if max>=0:
    	           word_nm2=word_nm2[:max+1]
    	           word_nm2=re.sub(ur"[^%s]"%infixes, '*',word_nm2)
    	       if word_nm2.count('*')>=3:
    	           return -1120;

    	       if word_nm2.find(u'*%s*'%ALEF)>=0:

    	           return -1130;
    # case of meem has three original letters in folloing
    	if re.search(u"^([^\*])*%s"%(MEEM),starword) and starword.count('*')>=3:
    	   return -1140;
    # case of meem folowed by t, noon, st, has two original letters in folloing
    	if re.search(u"^([^\*])*%s(%s|%s|%s%s)"%(MEEM,TEH,NOON,SEEN,TEH),starword) and starword.count('*')>=2:
    	   return -1145;


    # the word is finished by ALEF TEH
    # and the  original letters are more than two,
    	if re.search(u"%s%s([^\*])*$"%(ALEF,TEH),starword) and starword.count('*')>=3:
    	           return -1150;

    # the word contains **Y* when y is Yeh
    	if re.search(ur"\*\*%s\*"%(YEH),starword) :
    	    return -1160;
    # the word contains al*Y* when ALEF-LAM+*+yeh+*is Yeh
    	if re.search(ur"%s%s\*%s\*"%(ALEF,LAM,YEH),starword) :

    	    return -1170;
    # the word contains al*w* when ALEF-LAM+*+WAW+*  w is Waw
    	if re.search(ur"%s%s\*%s\*"%(ALEF,LAM,WAW),starword) :

    	    return -1180;

    # the word contains ***w* when ***+WAW+* w is Waw
    	if re.search(ur"[^%s]\*\*%s\*"%(u"تاينلفأو",WAW),starword) :

    	    return -1190;
    # the word contains **a* when **+a+* a is alef
    	if re.search(ur"\*[\*%s]%s\*"%(u"وي",ALEF),starword) :

    	    return -1200;
    # the word contains t**y* when **+t+* a is alef
    	if re.search(ur"%s\*\*%s\*"%(TEH,YEH),starword) :

    	    return -1210;
    # case of word ends  with ALEf noon, if it hasnt Yeh or teh on prefix
    	if re.search(u"^([^\*%s%s])*\*"%(YEH,TEH),starword) and re.search(u"%s%s([^\*%s%s])*$"%(ALEF,NOON,ALEF,YEH),starword) and starword.count("*")>=2:
    	    return -1220;

    # case of word ends  with waw noon, if it hasnt Yeh or teh on prefix
    	if re.search(u"^([^\*%s%s%s%s])*\*"%(YEH,TEH,ALEF_HAMZA_ABOVE,ALEF),starword) and re.search(u"%s%s([^\*%s%s])*$"%(WAW,NOON,ALEF,YEH),starword) and starword.count("*")>=2:
    	    return -1230;
    # case of word ends  with YEH noon, if it hasnt Yeh or teh on prefix
    	if re.search(u"^([^\*%s%s%s%s])*\*"%(YEH,TEH,ALEF_HAMZA_ABOVE,ALEF),starword) and re.search(u"%s%s([^\*%s%s])*$"%(YEH,NOON,ALEF,YEH),starword) and starword.count("*")>=2:
    	    return -1230;

    # the word is finished by waw-noon, alef-noon, yeh-noon, and not started by ALEF_HAMZA_ABOVE or YEH or TEH or NOON,
    # and the stem length is more than 2 letters
    # and not have verb prefixes WAW, FEH, LAM,SEEN

    #ToDo 2 avoid فكان وفزين cases
    	if re.match(ur"^[%s|%s]?[%s|%s]?((.){2,7})(%s|%s|%s)%s$"%(FEH,WAW,SEEN,LAM,WAW,YEH,ALEF,NOON),word_nm):
    	   if not re.match(ur"^[%s|%s]?[%s|%s]?[%s%s%s%s%s%s]"%(FEH,WAW,SEEN,LAM,YEH,TEH,ALEF_HAMZA_ABOVE,ALEF_MADDA,NOON,ALEF),word_nm):
    	       return -1100;



    	return 100;


    def guess_stem(self,word):
        """
        Detetect affixed letters based or phonetic root composition.
        In Arabic language, there are some letters which can't be adjacent in a root.
        This function return True, if the word is valid, else, return False

        @param word: the word.
        @type word: unicode.
        @return: word with a '-' to indicate the stemming position.
        @rtype: unicode
        """
    # certain roots are forbiden in arabic
    #exprimed in letters sequences
    # but this sequence can be used for affixation
    #then we can guess that this letters are affixed
    #
    #treat one prefixe letter
    # we strip harkat and shadda
        word=ar_strip_marks(word);
        prefixes_letters=(TEH, MEEM,LAM,WAW,BEH, KAF,FEH,HAMZA,YEH,NOON)
        prefixes_forbiden={
        ALEF_HAMZA_ABOVE:(ALEF_HAMZA_ABOVE,ZAH,AIN,GHAIN),
        BEH:(BEH,FEH,MEEM),
        TEH:(THEH,DAL,THAL,ZAIN,SHEEN,SAD,DAD,TAH,ZAH),
        FEH:(BEH,FEH,MEEM),
        KAF:(JEEM,DAD,TAH,ZAH,QAF,KAF),
        LAM:(REH,SHEEN,LAM,NOON),
        MEEM:(BEH,FEH,MEEM),
        NOON:(REH,LAM,NOON),
        WAW:(WAW,YEH),
        YEH:(THEH,JEEM,HAH,KHAH,THAL,ZAIN,SHEEN,SAD,DAD,TAH,ZAH,GHAIN,KAF,HEH,YEH),
            }

        word_guess=word;
        if len(word)>=2:
            c1=word[0];
            c2=word[1];
            if c1 in prefixes_letters and ( c2 in prefixes_forbiden[c1]):
                word_guess=u"%s-%s"%(c1,word[1:])
                if len(word_guess)>=4:
                    c1=word_guess[2];
                    c2=word_guess[3];
                    if c1 in prefixes_letters and ( c2 in prefixes_forbiden[c1]):
                        word_guess=u"%s-%s"%(c1,word_guess[2:])




    # treat two suffixe letters
        bisuffixes_letters=(KAF+MEEM,KAF+NOON,HEH+MEEM,HEH+NOON)

        bisuffixes_forbiden={
        HEH+MEEM:(ALEF_HAMZA_ABOVE,HAMZA,WAW_HAMZA,YEH_HAMZA,BEH,THEH,HAH, KHAH, SAD, DAD, TAH,ZAH,AIN,GHAIN,HEH,YEH),
        KAF+MEEM:(ALEF_HAMZA_ABOVE,HAMZA,WAW_HAMZA,YEH_HAMZA,BEH,THEH,JEEM, KHAH,ZAIN,SEEN, SHEEN,DAD, TAH,ZAH,GHAIN, FEH, QAF,KAF, LAM, NOON, HEH,YEH),
        HEH+NOON:(ALEF_HAMZA_ABOVE,HAMZA,WAW_HAMZA,YEH_HAMZA,BEH,THEH,JEEM,HAH, KHAH, SAD, DAD, TAH,ZAH,AIN,GHAIN,HEH,YEH),
        KAF+NOON:(ALEF_HAMZA_ABOVE,HAMZA,WAW_HAMZA,YEH_HAMZA,BEH,THEH,JEEM,HAH, KHAH,THAL,SHEEN,DAD, TAH,ZAH,AIN, GHAIN, QAF,KAF, NOON, HEH,YEH),

            }
    ##    word_guess=word;
        word=word_guess;
        if len(word)>=3:
            bc_last=word[-2:];
            bc_blast=word[-3:-2]
            if bc_last in bisuffixes_letters:
                if bc_blast in bisuffixes_forbiden[bc_last]:
                    word_guess=u"%s-%s"%(word[:-2],bc_last)

    # treat one suffixe letters
        suffixes_letters=(KAF,TEH,HEH)

        suffixes_forbiden={
        TEH:(THEH,JEEM,DAL,THAL,ZAIN,SHEEN,TAH,ZAH),
        KAF:(THEH,JEEM,KHAH, THAL,TAH,ZAH,GHAIN,QAF),
        HEH:(TEH,HAH,KHAH,DAL,REH,SEEN,SHEEN,SAD,ZAH,AIN,GHAIN),
            }
        word=word_guess;
        c_last=word[-1:];
        c_blast=word[-2:-1]
        if c_last in suffixes_letters:
            if c_blast in suffixes_forbiden[c_last]:
                word_guess=u"%s-%s"%(word[:-1],c_last)


        return word_guess;


    def is_valid_stem(self,stem):
        """
        Return True if the stem is valid.
        A stem can't be started by SHADDA, WAW_HAMZA, YEh_HAMZA.
        @param stem: the stem.
        @type stem: unicode.
        @return: is valid a tsem.
        @rtype: Boolean
        """

    	if stem[0] in (WAW_HAMZA,YEH_HAMZA,SHADDA):
    		return False;
    	stem_guessed=guess_stem(stem);
    	if re.search("-",stem_guessed):
    		return False;
    	return True;


    def context_analyse(self,word_one, word_two):
        """
        Detect the word type according to the previous word.
        @param word_one: the previous word.
        @type word_one: unicode.
        @param word_two: the word to detect.
        @type word_two: unicode.

        @return: a code of word type ('v': verb, 'vn': verb& noun, 'n': noun)
        @rtype: unicode
        """

        tab_noun_context=(
        u"في",
        u"بأن",
        u"بين",
        u"ففي",
        u"وفي",
        u"عن",
        u"إلى",
        u"على",
        u"بعض",
        u"تجاه",
        u"تلقاء",
        u"جميع",
        u"حسب",
        u"سبحان",
        u"سوى",
        u"شبه",
        u"غير",
        u"كل",
        u"لعمر",
        u"مثل",
        u"مع",
        u"معاذ",
        u"نحو",
        u"خلف",
        u"أمام",
        u"فوق",
        u"تحت",
        u"يمين",
        u"شمال",
        u"دون",
        u"من",
        u"بدون",
        u"خلال",
        u"أثناء",
        )
        tab_verb_context=(
        u"قد",
        u"فقد",
        u"وقد",
        u"لن",
        u"لم",
        )
        if word_one in tab_verb_context: return "v";
        elif word_one in tab_noun_context: return "n";
        elif word_two in tab_noun_context or word_two in tab_noun_context:
            return "t";
        return "vn";



    def is_stopword(self,word):
        """
        Return True if the word is a stopword, according a predefined list.
        @param word: the previous word.
        @type word: unicode.

        @return: is the word a stop word
        @rtype: Boolean
        """
        if word in STOPWORDS.keys():
            return True;
        else:
            return False;

