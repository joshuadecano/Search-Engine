from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, InvertedIndex
from text import BasicTokenProcessor, englishtokenstream

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = BasicTokenProcessor()
    vocabulary = set()
    tdi = InvertedIndex(vocabulary, len(corpus))
    for c in corpus:
        tokensz = englishtokenstream.EnglishTokenStream(c.get_content())
        for n in tokensz:
            itt = token_processor.process_token(n)
            vocabulary.add(itt)
            tdi.add_term(itt, c.id)
    return tdi

if __name__ == "__main__":
    corpus_path = Path()
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
    # Build the index over this directory.
    index = index_corpus(d)
    # We aren't ready to use a full query parser;
    # for now, we'll only support single-term queries.
    #query = "whale" # hard-coded search for "whale"\
    #print(index.get_postings("whale"))
    query = ""
    while query != "quit":
        query = input("Enter a word: ")
        for p in index.get_postings(query):
            print(f"Document ID {p.doc_id}")
