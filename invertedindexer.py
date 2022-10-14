from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, PositionalInvertedIndex
from text import protokenprocessor, englishtokenstream
from porter2stemmer import Porter2Stemmer
from queries import booleanqueryparser
import re
import time

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def stem_this(firstphrase : str) -> str:
    stemmer = Porter2Stemmer()
    secondphrase = []
    final_phrase = ""
    for t in firstphrase.split(" "):
        tok = t.strip()
        if len(tok) > 0:
            print(tok)
            if not tok[0].isalnum():   # removes the first letter if its not alphanumeric
                tok = tok[1:]
            if not tok[-1].isalnum():  # removes the last letter if its not alphanumeric
                tok = tok[:-1]
                temp = stemmer.stem(tok)
                print(temp)
                secondphrase.append(temp)
    #for s in secondphrase: 
    #    final_phrase += " "
    #    final_phrase += temp 

    return " ".join(secondphrase)
    #return final_phrase

def index_corpus(corpus : DocumentCorpus) -> Index:
    whitespace_re = re.compile(r"\W+")
    token_processor = protokenprocessor.ProTokenProcessor()
    vocabulary = set()
    tdi = PositionalInvertedIndex(vocabulary, len(corpus))
    #nums = 1
    for c in corpus:
        #nums += 1 
        #print(nums)
        tokensz = englishtokenstream.EnglishTokenStream(c.get_content())
        dex = 0             # new for proj
        for n in tokensz:
            #temp = re.sub(whitespace_re, "", n).lower()    
            temp = n.lower()
            if len(temp) != 0:
                itt = token_processor.process_token(n)
                if itt is not None:
                    for s in itt:
                        vocabulary.add(s)
                        tdi.add_term(s, c.id, dex)
                        dex += 1        # increments by 1 for every token passed in to add_term
    return tdi

if __name__ == "__main__":
    start = time.time()
    corpus_path = Path()
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
    index = index_corpus(d)
    stop = time.time()
    print("Indexing took", stop-start, "seconds")
    query = ""
    bqparser = booleanqueryparser.BooleanQueryParser()
    while query != ":q":
        query = input("Enter a query: ")
        stemmer = Porter2Stemmer()                                      # creates the stemmer object
        #token_processor = protokenprocessor.ProTokenProcessor()         # creates the token processor object
        #proc = token_processor.process_token(query)     #returns a list of words which have been processed (fires in yosemite) -> (fire in yosemit)
        #print("proc:", proc)
        if query[0] == '"' and query[-1] == '"':
            query = stem_this(query)  
        #query = stem_this(query)                     # stems the list of words
        print("fin_query:", query)                            # prints the final list of words which are stemmed
        book = bqparser.parse_query(query)          # this will return a query component, basically holds a list of postings
        if query.startswith(':stem'):
            token_processor = protokenprocessor.ProTokenProcessor()       # even though this already stems the word, I kept it just in case there was a typo maybe
            token = ' '.join(query.split()[1:])
            print(stemmer.stem(token))
            continue
        if query.startswith(':index'):
            token_processor = protokenprocessor.ProTokenProcessor()
            token = ' '.join(query.split()[1:])
            continue
        if query.startswith(':vocab'):
            testss = sorted(index.vocabulary())
            for i in range(1000):
                print(testss[i])
            print(f"Total number of vocabulary terms: {len(testss)}")
            continue
        if book is not None:                            # if there are no query results
            big_book = book.get_postings(index)         # returns a list of postings
            if big_book is None:
                print("Term not found")
            else:
                count = 1
                for s in big_book:
                    print("Document #", count, d.get_document((s.doc_id)))
                    count += 1
                print(len(big_book), "Documents found containing", query)
                answer = 1
                while answer != 0:
                    try:
                        answer = int(input("To view a document, enter the Document #, else enter '0'\n"))
                        if answer == 0:
                            continue
                        if int(answer) <= len(big_book):
                            print("Title:", d.get_document(big_book[answer-1].doc_id).title)
                            print(d.get_document(big_book[answer-1].doc_id).get_content().getvalue())
                        else:
                            print("Invalid selection")
                    except:
                        print("Invalid input")
            #biik = d.get_document(book.get_postings(index).doc_id)
            #print(type(biik))
            #for p in biik:
                #print(type(p))
                #print("seven")
                #anothaone = p.get_postings(index)
                #for s in anothaone:
                    #print("s")
                    #print(d.get_document(s.doc_id))
                #print(d.get_document(p.get_postings(index)))
                #test = d.get_document(p.get_postings(index))
                #for s in test:
                #    print(d.get_document(s.doc_id).title)
            #print(d.get_document(book.get_postings(index))

##        if book is not None:
##            count = 1
##            big_book = book.get_postings(index)
##            for p in big_book:
##                print("Document #", count, d.get_document(p.doc_id).title)
##                count += 1
##            print(len(big_book), "Documents found containing", query)
##            answer = 1
##            while answer != 0:
##                try:
##                    answer = int(input("To view a document, enter the Document #, else enter '0'\n"))
##                    if answer == 0:
##                        continue
##                    if int(answer) <= len(big_book):
##                        print("Title:", d.get_document(big_book[answer-1].doc_id).title)
##                        print(d.get_document(big_book[answer-1].doc_id).get_content().getvalue())
##                    else:
##                        print("Invalid selection")
##                except:
##                    print("Invalid input")
        else:
            print("no results")
