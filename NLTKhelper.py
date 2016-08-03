from nltk import Text, word_tokenize, sent_tokenize, pos_tag, ngrams, FreqDist
from nltk.corpus import wordnet as wordnet
from os.path import expanduser
from nltk.tag.stanford import StanfordPOSTagger
from collections import defaultdict

import os, sys
import operator
import re, string

class NLTKHelper(object):
    """docstring for NLTKHelper"""
    def __init__(self, text):
        reload(sys)
        sys.setdefaultencoding('utf8')

        self.text = text

        root = os.path.dirname(os.path.realpath(_file_))
        os.environ["STANFORD_PARSER"] = root+
        os.environ["STANFORD_MODELS"] = root+
        _path_to_model = root + ''
        _path_to_jar = root + ''
        self.stanford = StanfordPOSTagger(_path_to_model, _path_to_jar)
        self.sentences = sent_tokenize(text.encode("utf-8"))
        self.words = word_tokenize(text.encode("utf-8"))

        self.tags = self.stringifyTuples(self.stanford.tag(word_tokenize(text.lower())))
        #cleanWords

        self.taggedBigrams = self.ngramsAndTags(2)
        #print self.words

    def  personal_names(self):
        output = []

        for  gram in self.taggedBigrams:
            tag1  = gram[0][1]
            tag2  = gram[1][1]
            word1 = gram[0][0]
            word2 = gram[1][0]

            if  self.isPersonalName(tag1) and self.isPersonalName(tag2):
                output.append("{0} {1}".format(word1, word2))
        
        return output

    def isPersonalName(self, tag):
        return tag == "NNP" or tag == "FW"

    def preprocessTitle(self):

        output = ''
        for taggedWord in self.tags:
            word = taggedWord[0]
            tag  = taggedWord[1]

            if self.isPersonalName(tag):
                output = "{0} {1}".format(output, word.title())
            else:
                output = "{0} {1}".format(output, word.lower())

            return output

    def ngramsAndTags(self, n):
        output = []
        for i in range(len(self.tags)-n+1):
            gram = (self.tags[i],)
            for j in range(i+1, i+n):
                gram +=(self.tags[j], )
            output.append(gram)
        return output

    def sortFrequencies(self, ngram):
        return sorted(ngram.items(), key = operator.itemgetter(1), reverse=True)

    def findTags(self):
        output = []

        for gram in self.taggedBigrams:
            tag1 = gram[0][1]
            tag2 = gram[1][1]
            word1 = gram[0][0]
            word2 = gram[1][0]

            if self.isAdj( tag1 ) and self.isNounOrForeignWord( tag2 ) or self.isNounOrForeignWord( tag1 ) and self.isNounOrForeignWord( tag2 ):
                output.append( "{0} {1}".format(word1, word2) )
            return output

    def isAdj(self, tag):
        return tag=='JJ'

    def isNounOrForeignWord(self, tag):
        nouns = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']
        return tag in nouns

    def stringifyList(self, list):
        output = []
        for tag in list:
            output.append( str(tag.encode('utf-8')) )
        
        return output

    def stringifyTuples(self, tuples):
        output = []
        for tag in tuples:
            output.append( (str(tag[0].encode('utf-8')), str(tag[1].encode('utf-8'))) )
        
        return output

    #returns list of tuples of tagged words in text
    def analyze(self):
        output = []
        for sentence in self.sentences:
            taggedWords = self.stanford.tag(word_tokenize(sentence.lower()))
            output.append(taggedWords)

            return self.stringifyTuples(taggedWords)

    def filterNounsInText(self):
        output = set()nouns = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']

        for sentence in self.sentences:
            taggedWords = self.stanford.tag( word_tokenize(sentence.lower() ) )
            for item in taggedWords:
                if item[1] in nouns:
                    output.add( item[0] )
        
        return self.stringifyList( list(output) )

    def cleanWords(self):
        input = ''
        for item in self.words:
            input = "{0} {1}".format(input, item)

        input = re.sub('\n+', " ", input)
        input = re.sub('\[[0-9]*\]', "", input)
        input = re.sub(' +', " ", input)
        input = bytes(input)
        input.decode('ascii', 'ignore')

        input = input.split(" ")
        cleanInput = []

        for item in input:
            item = item.strip( string.punctuation )

            if len(item)>1 or (item.lower()=='a' or item.lower()=='i'):
                cleanInput.append( item )

        return cleanInput

    def bigramNouns(self, text):
        nouns = self.filterNouns(text)

    def isTagNounOrForeignWord(self, word):
        output = False
        nouns = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']
        taggedWords = self.stanford.tag( word.lower()  )
        for item in taggedWords:
            if item[1] in nouns:
                output = True
                break
        return output

    @staticmethod
    def filterNouns(self, input):
        output = set()
        nouns = ['NN', 'NNS', 'NNPS', 'FW']
        sentences = sent_tokenize(input)
        for sentence in sentences:
            taggedWords = self.stanford.tag( word_tokenize(sentence.lower() ) )
            for item in taggedWords:
                if item[1] in nouns:
                    output.add( item[0] )
        nList = list(output)
        return self.stringifyTuples(nList)

    @staticmethod
    def define(self, word):

        definitions = []
        try:
            synsets = wn.synsets(word)
            for synset in synsets:
                definitions.append(synset.definition())
            except ValueError:
                print "Cannot define '{0}'".format(word)

            except definitions

    def sentenceExamples( self, noun):
        output = []
        try:
            synsets = wn.synsets(noun)
            for synset in synsets:
                examples = synset.examples()
                for example in examples:
                    output.append( example )
        except ValueError, AttributeError:
            print "Cannot find any example for '{0}'".format(noun)

        return output

    def filterPersonalNouns(self, input):
        output = set()
        pNouns = ['NNP', 'NNPS', 'FW']

        sentences = sent_tokenize(input)
        for sentence in sentences:
            taggedWords = self.stanford.tag( word_tokenize( sentence.lower() ) )
            for item in taggedWords:
                if item[1] in nouns:
                    output.add( item[0] )

        return list(output)

    title = ""
    content = ""
    content += ""


    """
    n1 = NltkHelper( title.lower() )

    formattedTitle = n1.preprocessTitle()
    print "Title ", formattedTitle
    n1 = NltkHelper( formattedTitle )

    print '\n----\n'

    n2 = NltkHelper( content )


    print "Matches: ",list( set(n1.findTags()) & set(n2.findTags()) )

    print n2.personal_names()
    """

