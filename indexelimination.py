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
    for t in firstphrase.split(" "):
        tok = t.strip()
        if len(tok) > 0:
            if not tok[0].isalnum():   # removes the first letter if its not alphanumeric
                tok = tok[1:]
            if not tok[-1].isalnum():  # removes the last letter if its not alphanumeric
                tok = tok[:-1]
            temp = stemmer.stem(tok)
            secondphrase.append(temp)
    return '"' + " ".join(secondphrase) + '"'

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
    threshold = 2.5
    for s in phrase.split(" "): # for each term in query
        term = s.strip()
        cursor.execute("SELECT position FROM bytes WHERE terms = (?)", (term, ))
        target_byte = cursor.fetchone()
        if target_byte == None:
            continue
        term_postings = index.get_no_postings(term) # posting list for each term
        f.seek(target_byte[0])
        dft = struct.unpack('i', f.read(4))[0] # unpacks dft
        f.seek(4,1) # skips id to find tftd 
                    # now it will be skipping ID to find wdt
        wqt = float(np.log(1+(n/dft)))
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
        #print(corpus.get_document(docids), " -- ", z)
        temp = corpus.get_document(docids)
        file_names.append(temp.title)
    return file_names

def relevant(qrel : list, doc : str) -> int:
    if doc in qrel:
        return 1
    else:
        return 0

def average_precision(query : str, qrel : list, doc_list : list) -> list:
    ap = 0
    counter = 0
    rel_counter = 0
    rel = len(qrel)
    for doc in range(len(doc_list)):
        if doc_list[doc] in qrel:
            relevance = 1
            rel_counter += 1
            doc_list[doc] = doc_list[doc] + " - Relevant"
        else:
            relevance = 0
        counter += 1
        ap += relevance * (rel_counter/counter)
    ap = ap/rel
    doc_list.append(ap)
    return doc_list


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
                        if s in hashmap:
                            hashmap[s] += 1     # if the term is already in the hashmap keys add 1 to the counter
                        else:
                            hashmap[s] = 1      # if the term is not yet in the hashmap, set it to 1
                        tdi.add_term(s, c.id, dex)
                        
                        dex += 1        # increments by 1 for every token passed in to add_term
        # this is after the document is done being indexed
        for tftd in hashmap.values():
            temp = (1 + np.log(tftd))
            wdt_sum += temp**2
        ld = math.sqrt(wdt_sum)
        waitlist[c.id] = float(ld)
    stop = time.time()
    print("time it took to index: ", stop - start)
    tdi.vocabular.sort()
    start2 = time.time()
    diw.write_index(tdi, corpus_path, waitlist)
    stop2 = time.time()
    print("time it took to write index to disk: ", stop2 - start2)
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
            d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
            index = index_corpus(d)
            handled = True
        if index_question == "2":
            user_path = input("Enter corpus path: ")
            corpus_path = Path(user_path)
            os.chdir(user_path)
            test_path = corpus_path / "postings.bin"   # this checks to see if the current corpus path has already been indexed
            handled = True
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
    dpi = DiskPositionalIndex(corpus_path)
    print("1. Boolean retrieval.")
    print("2. Ranked retrieval.")
    retrieval_question = input("")

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
                newpath = query.split()[1:]
                print(newpath)
                corpus_path = Path(newpath)
                d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
                continue
            if query.startswith(':vocab'):
                connection = sqlite3.connect("bytepositions.db")
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
            if choice == "1":
                print("Enter a query by index:")
                query_index = int(input(""))
                query_tokens = []
                qrel = []
                # for each token in the query, we will process it and add it to a list
                for s in query_list[query_index].split():
                    if not s.isalnum():
                        continue
                    else:
                        query_tokens.append(token_processor.process_token(s)[0])
                fin_query = " ".join(query_tokens)
                for s in qrel_list[query_index].split():
                    doc_name = str(s).zfill(4)
                    next_path = corpus_path / str(doc_name + ".json")
                    with open(next_path, 'r', encoding="utf-8") as file:
                        jtitle = json.load(file)
                        title = jtitle["title"]
                        qrel.append(title)
                iterations = 0
                start = time.time()
                while (iterations < 30):
                    scores = cosine_score(fin_query, dpi, d, corpus_path)
                    iterations += 1
                stop = time.time()
                relret = average_precision(query_list, qrel, scores)
                doc_counter = 0
                if (len(relret) < 50):
                    print("Returned less than K=50 results")
                    print("Lower threshold and try again.")
                    print("")
                    continue
                while doc_counter < 50: 
                    print(relret[doc_counter])
                    doc_counter += 1
                print("Throughput for the query: ", iterations/(stop-start))
                print("Average Precision: ", relret[-1])
            if choice == "2":
                ap = 0
                map = 0
                start = time.time()
                query_count = len(query_list)
                # for each line in both files
                for i in range(query_count):
                    # for each line, qrel is a new list of doc names as integers
                    query_tokens = []
                    qrel = []
                    # for each token in the query, we will process it and add it to a list
                    for s in query_list[i].split():
                        if not s.isalnum():
                            continue
                        else:
                            query_tokens.append(token_processor.process_token(s)[0])
                    fin_query = " ".join(query_tokens)
                    for s in qrel_list[i].split():
                        doc_name = str(s).zfill(4)
                        # here I need to somehow turn the numbers (int(s)) into the file titles.
                        next_path = corpus_path / str(doc_name + ".json")
                        with open(next_path, 'r', encoding="utf-8") as file:
                            jtitle = json.load(file)
                            title = jtitle["title"]
                            qrel.append(title)
                    # passes in each query line
                    # and each relevant document line (by name)
                    scores = cosine_score(fin_query, dpi, d, corpus_path)
                    ap = average_precision(query_list, qrel, scores)[-1]
                    map += ap
                stop = time.time()
                mrt = (stop-start) / query_count
                print("Mean Response Time: ", mrt)
                throughput = query_count / (stop-start)
                print("Throughput: ", throughput)
                map = map/query_count
                print("Mean Average Precision: ", map)