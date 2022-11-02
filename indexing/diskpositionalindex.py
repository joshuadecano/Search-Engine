from .index import Index
from typing import Iterable
from indexing.postings import Posting
from pathlib import Path
import struct
import sqlite3

class DiskPositionalIndex(Index):
    def __init__(self, deva_path: Path, vocab : Iterable[str], corpus_size : int):
        self.vocabulary = list(vocab)
        self.vocabulary.sort()
        self.corpus_size = corpus_size
        #self.connection = sqlite3.connect("bytepositions.db") not sure if i need this
        self.path = open(deva_path,"rb")
    def get_postings(self, term : str) -> Iterable[Posting]:
        connection = sqlite3.connect("bytepositions.db")
        cursor = connection.cursor()
        target_byte = cursor.execute("SELECT position FROM bytes WHERE terms = (?)", term)
        self.path.seek(target_byte) # seek to the target_byte given by the query
        size = int(self.path.read(1))   # DFt
                                        # it will be read as a binary number and we need to set it to int
        posting_list = [None] * size # posting list we will return
        prev_docid = 0
        for s in size:  # for each doc containing the term
            self.path.seek(1,1) # seek to doc_id
            doc_id = struct.unpack('i', self.path.read(1)) #doc_id
            post = Posting(doc_id + prev_docid) #create a posting with the doc_id
            prev_docid = doc_id
            self.path.seek(1,1) # seek to tftd (number of positions)
            position_count = size = struct.unpack('i', self.path.read(1))
            prev_position = 0
            for t in position_count:
                self.path.seek(1,1) # seek to pi, (position of term in doc_id)
                position = struct.unpack('i', self.path.read(1))
                post.add_position(position + prev_position)
                prev_position = position
            posting_list.append(post)
        return posting_list
    #def add_term(self, term : str, doc_id : int):
    def vocabulary(self) -> Iterable[str]:
        return self.vocabulary