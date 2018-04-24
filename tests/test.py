from ar_adv import *
words=[u"سفاهة",
u"فسيكفيكهم",
u"غفورا",
u"وازدجر",
u"استيسر",
u"يابسات",
u"ألتناهم",
u"بسحركما",
u"بلادهتما",
u"أسقيناكموه",
u"ألهاكم",
u"سماكم",
u"أسقيناكم",
u"مكروها",
u"للمقوين",
u"سواها",

]
verb_prefix=u"مأسفلونيتاكب"
verb_infix=u"اتويدط"
verb_suffix=u"امتةكنهوي"
verb_max_prefix=6
verb_max_suffix=5
##word="fistf3l"
for word in words:
    print is_possible_verb(word);
    print is_possible_noun(word);
    word_nm=ar_strip_marks_keepshadda(word);

    starword=transformToStars(word_nm,verb_prefix,verb_suffix,verb_infix,verb_max_prefix,verb_max_suffix);
    print starword.encode("utf8")
##    print "\t",
    v_word=validate_affixes(starword);
    print v_word.encode("utf8")