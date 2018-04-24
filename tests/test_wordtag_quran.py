#!/usr/bin/python
# -*- coding=utf-8 -*-

import sys
import re
import string
import datetime
import  getopt
import os
import  naftawayh.wordtag
import naftawayh.wordtag_const
import sys
sys.path.append('naftawayh/lib');

exclusive_mode=False;
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
def usage():
# "Display usage options"
	print "(C) CopyLeft 2009, %s"%AuthorName
	print "Usage: %s -f filename [OPTIONS]" % scriptname
#"Display usage options"
	print "\t[-h | --help]\t\toutputs this usage message"
	print "\t[-V | --version]\tprogram version"
	print "\t[-f | --file= filename]\tinput file to %s"%scriptname
	print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
	all = False;
	segmentation=False;
	dictionarybased=False;
	templatesearch=False;
	rootextraction=False;
	vocalized=False;
	convert=False;
	fname = ''

	if not sys.argv[1:]:
		usage()
		sys.exit(0)
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hVdrtsv:f:",
                               ["help", "version","dict", "root", "template","all",
                                "seg", "vocalized", "file="],)
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for o, val in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit(0)
		if o in ("-V", "--version"):
			print scriptversion
			sys.exit(0)
		if o in ("-s", "--seg"):
			segmentation = True
		if o in ("-f", "--file"):
			fname = val
		if o in ("-d", "--dict"):
			dictionarybased = True
		if o in ("-r", "--root"):
			rootextraction=True;
		if o in ("-t", "--template"):

			templatesearch =True;
		if o in ("-v", "--vocalized"):
			vocalized =True;
		if o in ("-c", "--convert"):
			convert =True;
	return (fname,segmentation,dictionarybased,templatesearch,rootextraction,vocalized,convert)

def main():

	filename,segmentation,dictionarybased,templatesearch,rootextraction,vocalized,convert=grabargs()
	print "file name ",filename
#ToDo1 ref
	if (not filename):
		usage()
		sys.exit(0)
	option="";
	try:
		fl=open(filename);
	except :
		print " Error :No such file or directory: %s" % filename
		return None;
	line=fl.readline().decode("utf8");
	text=u""
	limit=12000;
	word_count=0;
	counter={
	"vn":0,
	"n=v":0,
	"!n!v":0,
	"v":0,
	"n":0,
	"t":0,
	"n1":0,
	"v1":0,
	"n2":0,
	};
	counter_match={
	"n":0,
	"v":0,
	"t":0,
	};	
	counter_quran={
	"n":0,
	"v":0,
	"t":0,
	"p":0,
	};
	rulecodeverbListUsed=[]
	rulecodenounListUsed=[]	
#--------------------------------------------
	tagger=naftawayh.wordtag.WordTagger();
	print '\t'.join(["tag","type_word","rulecodeverb","rulecodenoun","word"]);
	rulecodeverbList=naftawayh.wordtag_const.verbPattern.keys();
	rulecodenounList=naftawayh.wordtag_const.nounPattern.keys();
	
	while line and word_count<limit:
		line=fl.readline().decode("utf8");
		fields=line.split(";");
		if len(fields)>=2:
			word=fields[0];
			type_word_arabic=fields[1];
			if type_word_arabic.find(u"فعل")>=0: 
				type_word=u"v"

			elif type_word_arabic.find(u"اسم")>=0 :
				type_word=u"n"
			elif type_word_arabic.find(u"أداة")>=0 : 
				type_word=u"t"
			else:
				type_word=u"p"
			counter_quran[type_word]+=1;
			# count words
			word_count+=1;
			word=word.strip(u" ")
			# tag the word
			tag='';
			verbstamp="";
			stem="";
			rulecodeverb=0;
			rulecodenoun=0;
			if tagger.is_stopword(word):
				tag='t';
			elif tagger.is_specialword(word):
				tag='n1';				
				#print "ok1"
			else:
				#tagger.lightStemming(word);
				rulecodenoun=tagger.is_possible_noun(word)
				# if rulecodenoun<=0:
					# rulecodeverb=tagger.is_possible_verb(word);
				# else:
					# rulecodeverb=-10000;
				if exclusive_mode:
					if rulecodenoun<=0:
						rulecodeverb=tagger.is_possible_verb(word);
					else:
						rulecodeverb=-10000;
				else:
					rulecodeverb=tagger.is_possible_verb(word);
				
				if rulecodenoun==0 and rulecodeverb==0:
					tag="vn";
				elif( rulecodenoun>=0 and rulecodeverb<0) or (rulecodenoun>0 and rulecodeverb==0):
					tag="n";
				elif (rulecodeverb>=0 and rulecodenoun<=0) or  (rulecodeverb>0 and rulecodenoun==0) :
					tag="v";
				elif (rulecodeverb<0 and rulecodenoun<0) :
					tag="!n!v";
				elif (rulecodeverb>0 and rulecodenoun>0) :
					tag="n=v";
			counter[tag]+=1;
			if tag==type_word:
				counter_match[tag]+=1;
			if -rulecodeverb not in rulecodeverbListUsed:
				rulecodeverbListUsed.append(-rulecodeverb);
			if -rulecodenoun not in rulecodenounListUsed:
				rulecodenounListUsed.append(-rulecodenoun);
			
			print '\t'.join([tag,type_word,str(rulecodeverb),str(rulecodenoun),word]).encode('utf8');
	print "----",datetime.datetime.now(),"---"

	print "All words \t", word_count;
	for key in counter.keys():
		print "\t".join([str(key),str(counter[key]),str(counter[key]*100/word_count)+"%"]);
	print "Match \t";
	for key in counter_match.keys():
		print "\t".join([str(key),str(counter_match[key]),str(counter_match[key]*100/word_count)+"%"]);

	print "Quran words \t";
	for key in counter_quran.keys():
		print "\t".join([str(key),str(counter_quran[key]),str(counter_quran[key]*100/word_count)+"%"]);
	print "Used verb rules", 
	print rulecodeverbListUsed;
	print "Used noun rules", 
	print rulecodenounListUsed
	print "Unused verb rules ",set(rulecodeverbList).difference(set(rulecodeverbListUsed));
	print "Unused noun rules ", set(rulecodenounList).difference(set(rulecodenounListUsed));
	
if __name__ == "__main__":
  main()







