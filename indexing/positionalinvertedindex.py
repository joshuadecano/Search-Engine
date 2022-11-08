from bisect import bisect_left
from typing import Iterable
from pydoc import doc
from decimal import InvalidOperation
from .index import Index
from .postings import Posting

class PositionalInvertedIndex(Index):
    
    def __init__(self, vocab : Iterable[str], corpus_size : int):
        """Constructs an empty index using the given vocabulary and corpus size."""
        self.hasheroni = {}
        self.vocabular = list(vocab)
        #self.vocabular.sort()
        self.corpus_size = corpus_size
        #self.term_count = {}

    def add_term(self, term : str, doc_id : int, position : int):   #pass in the integer position of the term within the document in addition to the doc id and string
        # TO DO: rather than adding individual postings to the hashmap and just having the key as the term and the values as a list of postings of doc_ids with the term, 
        # we are now having the values as 
        # a list of posting objects which contain the doc_id and a list of positions within the doc that the word is in.
        post = Posting(doc_id)
        if term in self.hasheroni:                  #if the term is in the hash map keys
            if post.doc_id == self.hasheroni[term][-1].doc_id:            #if the document id is not the most recent item in the hash map values
                self.hasheroni[term][-1].add_position(position)         #add the document id to the list of postings
            else:
                post.add_position(position)
                self.hasheroni[term].append(post) #add doc to list 
        else:
            post.add_position(position)
            self.hasheroni[term] = [post]

        
    def get_postings(self, term : str) -> Iterable[Posting]:
        """Returns a list of Postings for all documents that contain the given term."""
        if term in self.hasheroni:
            return self.hasheroni[term]
    
    def vocabulary(self) -> Iterable[str]:
        return self.vocabular
