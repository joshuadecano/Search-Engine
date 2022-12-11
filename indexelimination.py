from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus, Document
from indexing import Index, PositionalInvertedIndex, diskindexwriter
from indexing.diskpositionalindex import DiskPositionalIndex
from text import protokenprocessor, englishtokenstream
from porter2stemmer import Porter2Stemmer
from queries import booleanqueryparser, querycomponent
from typing import Iterable
from queue import PriorityQueue
from io import StringIO
import json
import heapq as hq
import re
import os
import time
import math
import numpy as np
import sqlite3
import struct
import queue

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

def cosine_score(phrase : str, index : Index, corpus : DocumentCorpus, path = Path) -> Iterable[Document]:
    scores = {}
    heep = []
    file_names = []
    n = len(corpus.documents())
    connection = sqlite3.connect("bytepositions.db")
    sixth_path = path / "postings.bin"
    f = open(sixth_path,"rb")
    cursor = connection.cursor()
    threshold = .001
    for s in phrase.split(" "): # for each term in query
        term = s.strip()
        term_postings = index.get_no_postings(term) # posting list for each term
        cursor.execute("SELECT position FROM bytes WHERE terms = (?)", (term, ))
        target_byte = cursor.fetchone()
        f.seek(target_byte[0])
        dft = struct.unpack('i', f.read(4))[0] # unpacks dft
        f.seek(4,1) # skips id to find tftd 
                    # now it will be skipping ID to find wdt
        wqt = float(np.log(1+(n/dft)))
        print(wqt)
        if wqt < threshold:
            continue
        else:
            for t in term_postings: # for each document in term's posting list
                wdt = struct.unpack('d', f.read(8))[0]
                tftd = struct.unpack('i', f.read(4))[0]     # reads the tftd from file
                if t.doc_id not in scores.keys():
                    scores[t.doc_id] = 0
                scores[t.doc_id] += float(wqt * wdt)
                f.seek(((tftd*4)+4),1)    # jumps past the pi's and id to go back to tftd
    f.close()
    seventh_path = path / "docWeights.bin"
    g = open(seventh_path, "rb")
    for u in scores.keys():
        g.seek((8*u))
        ld = struct.unpack('d', g.read(8))[0]
        scores[u] = float(scores[u] / ld)
        g.seek(0,0)
    for k, v in scores.items():
        heep.append(v)
    topt = hq.nlargest(50, heep)
    for z in topt:
        docids = [k for k, v in scores.items() if v == z][0]
        print(corpus.get_document(docids), " -- ", z)
        temp = corpus.get_document(docids)
        file_names.append(temp.title)
    return file_names

    # this will be in a for loop which will pass in each 
    # query in the list as a str 
    # and each qrel as the total number of relevant
    # here i will be using qrel to count how many different numbers separated by whitespace are there
    # used as 1/(number found using method above)

    # checks if the index i of the list qrel is 
    # new notes: since I'll be passing in values from average_precision to here
    # I might not need query, and just need qrel as a separate list of numbers.
def relevant(i : int, qrel : list, doc : str) -> int:
    #print(qrel)
    #print(doc)
    #print("hello")
    if doc in qrel:
        print("NICE")
        return 1
    else:
        return 0

#def average_precision(query : str, qrel : int, i : int):
def average_precision(query : str, qrel : list, doc_list : list) -> float:
    # TO DO:
    # Keep a rolling value of precision @ i (precision)
    # this means I'll need a counter for documents returned (counter)
    # and also a counter for relevant items (rel_counter)
    # P@i = rel_counter / counter
    # ASSUMING THIS ONLY APPLIES TO TEST COLLECTIONS AND WE HAVE ALREADY INDEXED THE SELECTED FOLDER.
    # *since we don't have the qrel for the whole parks corpus

    # since we are already in the relevance____ 
    ap = 0
    counter = 0
    rel_counter = 0
    rel = len(qrel)
    #print("well")
    #print(doc_list)
    for doc in doc_list:
        rel_counter += relevant(counter, qrel, doc_list)
        print(rel_counter)
        counter += 1
        ap += relevant(counter, qrel, doc) * (rel_counter/counter)
        print(ap)
    ap = ap/rel
    return ap



def index_corpus(corpus : DocumentCorpus) -> Index:
    start = time.time()
    token_processor = protokenprocessor.ProTokenProcessor()
    vocabulary = []
    tdi = PositionalInvertedIndex(vocabulary, len(corpus))
    diw = diskindexwriter.DiskIndexWriter()
    waitlist = [0]*(len(corpus.documents()))
    for c in corpus:    # c is an individual document in the corpus
        tokensz = englishtokenstream.EnglishTokenStream(c.get_content())
        wdt_sum = 0
        hashmap = {}    # key = term, value = counting occurence of term in document
                        # hashmap will be empty after each document is processed
        dex = 0             # holds the position of each term
        for n in tokensz:   # n is the unprocessed token in list tokensz
            temp = n.lower()
            if len(temp) != 0:
                itt = token_processor.process_token(temp)
                if itt is not None:
                    for s in itt:   # s is the processed token in list itt
                        #print(s)
                        #if s == prev_term:
                        #if s not in tdi.vocabular:             # I now handle this in tdi.add_term
                        #    tdi.vocabular.append(s)
                        if s in hashmap:
                            hashmap[s] += 1     # if the term is already in the hashmap keys add 1 to the counter
                            #tdi.hasheroni[s][-1].add_position(dex)
                        else:
                            hashmap[s] = 1      # if the term is not yet in the hashmap, set it to 1
                            #tdi.add_term(s, c.id, dex)
                        #print(s)
                        tdi.add_term(s, c.id, dex)
                        
                        dex += 1        # increments by 1 for every token passed in to add_term
        # this is after the document is done being indexed
        for tftd in hashmap.values():
            temp = (1 + np.log(tftd))
            wdt_sum += temp**2
        ld = math.sqrt(wdt_sum)
        #print(ld)
        #print(c.id)
        waitlist[c.id] = float(ld)
    stop = time.time()
    print("time it took to index: ", stop - start)
    tdi.vocabular.sort()
    #print(tdi.vocabulary()[7])
    #print("corpus path: " , corpus_path)
    start2 = time.time()
    diw.write_index(tdi, corpus_path, waitlist)
    stop2 = time.time()
    print("time it took to write index to disk: ", stop2 - start)
    return tdi

if __name__ == "__main__":
    print("1. Build index.")
    print("2. Query index.")
    index_question = input("")
    handled = False
    corpus_path = ""

    while handled == False:
        if index_question == "1":     # indexes corpus to RAM and then writes it to disk
            user_path = input("Enter corpus path: ")
            corpus_path = Path(user_path)
            os.chdir(user_path)
            #start = time.time()
            d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
            index = index_corpus(d)
            #stop = time.time()
            #print("time it took to index: ", stop - start)
            handled = True
        if index_question == "2":
            user_path = input("Enter corpus path: ")
            corpus_path = Path(user_path)
            os.chdir(user_path)
            test_path = corpus_path / "postings.bin"   # this checks to see if the current corpus path has already been indexed
            #if os.path.exists(test_path) == True:
                #print("NICE SOMETHING WORKED")
                #print(corpus_path)
                #print("here now")
            handled = True
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
    #print(len(d.documents()))
    dpi = DiskPositionalIndex(corpus_path)
    #print(type(corpus_path))
    print("1. Boolean retrieval.")
    print("2. Ranked retrieval.")
    #print("3. Mean Average Precision.")
    retrieval_question = input("")

    # Begin retrieval
    #query = input("Enter a query")
    query = ""
    bqparser = booleanqueryparser.BooleanQueryParser()
    if retrieval_question == "1":
        while query != ":q":
            query = input("Enter a query: ")
            if query == ":q":
                break
            stemmer = Porter2Stemmer()                                      # creates the stemmer object
            if query[0] == '"' or query[-1] == '"':
                query = stem_this(query)
            fin_query = new_stem(query)
            print("Query after stemming:", fin_query)                            # prints the final list of words which are stemmed
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
                connection = sqlite3.connect("bytepositions.db")
                #sixth_path = corpus_path / "postings.bin"
                #f = open(sixth_path,"rb")
                cursor = connection.cursor()
                testss = dpi.vocabulary()
                cursor.execute("SELECT terms FROM bytes")
                testss = cursor.fetchall()
                print(len(testss))
                for i in range(1000):
                    print(testss[i])
                print(f"Total number of vocabulary terms: {len(testss)}")
                continue
            if book is not None:                            # if there are no query results
                big_book = book.get_postings(dpi)         # returns a list of postings
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
    if retrieval_question == "2":
        choice = ""
        # okay need to do this now
        token_processor = protokenprocessor.ProTokenProcessor()
        # lines of query as string
        query_list = []
        # lines of relevant files as a string (not int)
        qrel_list = []
        q_path = corpus_path / "relevance"
        with open(q_path / "queries") as file:
            for line in file:
                query_list.append(line.rstrip())
        with open(q_path / "qrel") as file:
            for line in file:
                qrel_list.append(line.rstrip())
        while choice != ":q":
            print("1. Query by index.")
            print("2. Mean Average Precision.")
            choice = input("")
            if choice == ":q":
                break
            #stemmer = Porter2Stemmer()                                      # creates the stemmer object
            #if query[0] == '"' or query[-1] == '"':
            #    query = stem_this(query)
            #fin_query = new_stem(query)
            if choice == "1":
                print("Enter a query by index:")
                query_index = int(input(""))
                query_tokens = []
                qrel = []
                # for each token in the query, we will process it and add it to a list
                for s in query_list[query_index].split():
                    query_tokens.append(token_processor.process_token(s)[0])
                fin_query = " ".join(query_tokens)
                for s in qrel_list[query_index].split():
                    holder = str(s + '.json')
                    #print(holder)
                    #f = open(holder)
                    #data = json.load(f)
                    #print(data["title"])
                    next_path = corpus_path / str(s+ ".json")
                    #print(next_path)
                    with open(next_path, 'r', encoding="utf-8") as file:
                        jtitle = json.load(file)
                        title = jtitle["title"]
                        #print(title)
                        qrel.append(title)

                scores = cosine_score(fin_query, dpi, d, corpus_path)
                #print(scores)
                app = average_precision(query_list, qrel, scores)
                print(app)
            if choice == "2":
                map = 0
                # for each line in both files
                for i in range(len(query_list)):
                    # for each line, qrel is a new list of doc names as integers
                    qrel = []
                    for s in qrel_list[i].split(" "):
                        # here I need to somehow turn the numbers (int(s)) into the file titles.
                        next_path = corpus_path / int(s) / ".json"
                        print(next_path)
                        with open(next_path, 'r', encoding="utf-8") as file:
                            jtitle = json.load(file)
                            title = StringIO(jtitle["title"])
                            print(title)
                            qrel.append(int(s))
                        
                    # passes in each query line
                    # and each relevant document line (by name)
                    scores = cosine_score(fin_query, dpi, d, corpus_path)
                    
                    map += average_precision(query_list, qrel, scores)
                print("Mean Average Precision: ", map)