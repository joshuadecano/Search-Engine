from bisect import bisect_left
from typing import Iterable
from pydoc import doc
from decimal import InvalidOperation
from .index import Index
from .postings import Posting

class InvertedIndex(Index):
    
    def __init__(self, vocab : Iterable[str], corpus_size : int):
        """Constructs an empty index using the given vocabulary and corpus size."""
        self.hasheroni = {}
        #self.posting_list = []
        self.vocabulary = list(vocab)
        self.vocabulary.sort()
        self.corpus_size = corpus_size

    def add_term(self, term : str, doc_id : int):
        post = Posting(doc_id)
        if term in self.hasheroni:                  #if the term is in the hash map keys
            if post.doc_id == self.hasheroni[term][-1].doc_id:            #if the document id is not the most recent item in the hash map values
                return None         #add the document id to the list of postings
            else:
                self.hasheroni[term].append(post) #add doc to list 
        else:
            self.hasheroni[term] = [post]

        
    def get_postings(self, term : str) -> Iterable[Posting]:
        """Returns a list of Postings for all documents that contain the given term."""
        if term in self.hasheroni:
            return self.hasheroni[term]
    
    def vocabulary(self) -> Iterable[str]:
        return self.vocabulary
