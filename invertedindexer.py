from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, PositionalInvertedIndex
from text import protokenprocessor, englishtokenstream
from porter2stemmer import Porter2Stemmer
from queries import booleanqueryparser
from io import StringIO
import re

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def index_corpus(corpus : DocumentCorpus) -> Index:
    whitespace_re = re.compile(r"\W+")
    token_processor = protokenprocessor.ProTokenProcessor()
    vocabulary = set()
    tdi = PositionalInvertedIndex(vocabulary, len(corpus))
    for c in corpus:
        tokensz = englishtokenstream.EnglishTokenStream(c.get_content())
        dex = 0             # new for proj
        for n in tokensz:
            temp = re.sub(whitespace_re, "", n).lower()    
            if len(temp) != 0:
                itt = token_processor.process_token(n)
                for s in itt:
                    vocabulary.add(s)
                    tdi.add_term(s, c.id, dex)
                    dex += 1        # increments by 1 for every token passed in to add_term
    return tdi

if __name__ == "__main__":
    corpus_path = Path()
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
    # Build the index over this directory.
    index = index_corpus(d)
    # We aren't ready to use a full query parser;
    # for now, we'll only support single-term queries.
    query = ""
    bqparser = booleanqueryparser.BooleanQueryParser()
    while query != ":q":
        query = input("Enter a query: ")
        stemmer = Porter2Stemmer()
        token_processor = protokenprocessor.ProTokenProcessor()  
        fin_query = (stemmer.stem(query))
        book = bqparser.parse_query(fin_query).get_postings(index)
        if query.startswith(':stem'):
            stemmer = Porter2Stemmer()
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
        if book is not None:
            if book is QueryComponent:
                
            count = 1
            for p in book:
                print("Document #", count, d.get_document(p.doc_id).title)
                count += 1
            print(len(book), "Documents found containing", query)
            answer = 1
            while answer != 0:
                try:
                    answer = int(input("To view a document, enter the Document #, else enter '0'\n"))
                    if answer == 0:
                        continue
                    if int(answer) <= len(book):
                        print("Title:", d.get_document(book[answer-1].doc_id).title)
                        print(d.get_document(book[answer-1].doc_id).get_content().getvalue())
                    else:
                        print("Invalid selection")
                except:
                    print("Invalid input")
        else:
            print("no results")
