from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, PositionalInvertedIndex, diskindexwriter
from indexing.diskpositionalindex import DiskPositionalIndex
from text import protokenprocessor, englishtokenstream
from porter2stemmer import Porter2Stemmer
from queries import booleanqueryparser, querycomponent
import re
import os
import time
import math
import numpy as np

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def stem_this(firstphrase : str) -> str:
    stemmer = Porter2Stemmer()
    secondphrase = []
    final_phrase = ""
    for t in firstphrase.split(" "):
        tok = t.strip()
        if len(tok) > 0:
            #print(tok)
            if not tok[0].isalnum():   # removes the first letter if its not alphanumeric
                tok = tok[1:]
            if not tok[-1].isalnum():  # removes the last letter if its not alphanumeric
                tok = tok[:-1]
            temp = stemmer.stem(tok)
            #print(temp)
            secondphrase.append(temp)
    return '"' + " ".join(secondphrase) + '"'
    #return final_phrase

def new_stem(firstphrase : str) -> str:
    stemmer = Porter2Stemmer()
    secondphrase =[]
    for t in firstphrase.split(" "):
        tok = t.strip()
        if len(tok) > 0:
            token = stemmer.stem(tok)
            secondphrase.append(token)
            
    return " ".join(secondphrase)

def index_corpus(corpus : DocumentCorpus) -> Index:
    whitespace_re = re.compile(r"\W+")
    token_processor = protokenprocessor.ProTokenProcessor()
    vocabulary = []
    tdi = PositionalInvertedIndex(vocabulary, len(corpus))
    diw = diskindexwriter.DiskIndexWriter()
    waitlist = []
    count = 1
    for c in corpus:    # c is an individual document in the corpus
        count+=1
        tokensz = englishtokenstream.EnglishTokenStream(c.get_content())
        wdt_sum = 0
        hashmap = {}    # key = term, value = counting occurence of term in document
                        # hashmap will be empty after each document is processed
        dex = 0             # holds the position of each term
        for n in tokensz:   # n is the unprocessed token in list tokensz
            temp = n.lower()
            if len(temp) != 0:
                itt = token_processor.process_token(n)
                if itt is not None:
                    for s in itt:   # s is the processed token in list itt
                        #print(s)
                        #if s == prev_term:
                        if s not in tdi.vocabular:
                            tdi.vocabular.append(s)
                        if s in hashmap:
                            hashmap[s] += 1     # if the term is already in the hashmap keys add 1 to the counter
                        else:
                            hashmap[s] = 1      # if the term is not yet in the hashmap, set it to 1
                        tdi.add_term(s, c.id, dex)
                        
                        dex += 1        # increments by 1 for every token passed in to add_term

                        # note: i will call the diskindexwriter somewhere here, where i should be passing in the calculated weight to
                        # be added to the file docWeights.bin
                        # things we will need to know here
                        # tftd
                        # i could use len(tdi.hasheroni[term]) since tdi.hasheroni[term] should return a list of positions of the term in the doc
                        # actually maybe not since it actually holds a list of postings, maybe if i could access those postings and get the
                        # length of 
        # this is after the document is done being indexed
        for tftd in hashmap.values():
            temp = (1 + np.log(tftd))
            wdt_sum += temp**2
        ld = math.sqrt(wdt_sum)
        #print(ld)
        #print(c.id)
        waitlist.append(float(ld))
    tdi.vocabular.sort()
    print(tdi.vocabulary()[7])
    diw.write_index(tdi, corpus_path, waitlist)
    return tdi

if __name__ == "__main__":
    print("1. Build index.")
    print("2. Query index.")
    #newq = ""
    index_question = input("")
    handled = False
    #start = time.time()
    while handled == False:
        if index_question == "1":     # indexes corpus to RAM and then writes it to disk
            user_path = input("Enter corpus path: ")
            corpus_path = Path(user_path)
            #start = time.time()
            d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
            index = index_corpus(d)
            handled = True
        if index_question == "2":
            user_path = input("Enter corpus path: ")
            corpus_path = Path(user_path)
            test_path = corpus_path / "postings.bin"   # this checks to see if the current corpus path has already been indexed
            
            
            if os.path.exists(test_path) == True:
                print("NICE SOMETHING WORKED")
                print(corpus_path)
                d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
                print(len(d.documents()))
                dpi = DiskPositionalIndex(corpus_path)      # i can probably move this out of this while loop since dpi only requires the path and the index should be built already
                print("here now")
                big_book = dpi.get_postings("moos")         # returns a list of postings
                if big_book is None:
                    print("Term not found")
                else:
                    count = 1
                    print(len(big_book))
                    #print(big_book)
                    for s in big_book:
                        #print(s.doc_id)
                        print("Document #", count, d.get_document((s.doc_id)))
                        count += 1
                    #print(len(big_book), "Documents found containing", query)
                    
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
                handled = True
            else:
                print("This directory has does not contain a corpus")
                print("boutta build one for u though")
                d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
                stop = time.time()
                print("Indexing took", stop-start, "seconds")
                start = time.time()
                index = index_corpus(d)
                stop = time.time()
                print("Time writing to disk:", stop - start, "seconds")
                handled = True
    
    print("1. Boolean retrieval.")
    print("2. Ranked retrieval.")
    retrieval_question = input("")
            

    #user_path = input("Enter corpus path: ")
    #corpus_path = Path(user_path)
    #start = time.time()
    #d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
    #index = index_corpus(d)
    #stop = time.time()
    #print("Indexing took", stop-start, "seconds")
    query = input("")
    bqparser = booleanqueryparser.BooleanQueryParser()
    while query != ":q" and retrieval_question == 1:
        if query == ":q":
            break
        query = input("Enter a query: ")
        stemmer = Porter2Stemmer()                                      # creates the stemmer object
        if query[0] == '"' or query[-1] == '"':
            query = stem_this(query)
        fin_query = new_stem(query)
        print("Query after stemming:", query)                            # prints the final list of words which are stemmed
        book = bqparser.parse_query(fin_query)          # this will return a query component, basically holds a list of postings
        if query.startswith(':stem'):
            token_processor = protokenprocessor.ProTokenProcessor()       # even though this already stems the word, I kept it just in case there was a typo maybe
            token = ' '.join(query.split()[1:])
            print(stemmer.stem(token))
            continue
        if query.startswith(':index'):
            #token_processor = protokenprocessor.ProTokenProcessor()
            newpath = query.split()[1:]
            print(newpath)
            corpus_path = Path(newpath)
            d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
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
        else:
            print("no results")
    while query != ":q" and retrieval_question == 2:
        print("okay need to do this now")
