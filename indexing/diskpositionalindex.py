from .index import Index
from typing import Iterable
from indexing.postings import Posting
from pathlib import Path
import struct
import sqlite3

class DiskPositionalIndex(Index):
    def __init__(self, deva_path: Path): # I took out ", vocab : Iterable[str], corpus_size : int" because i dont think we need it
        #self.vocabulary = list(vocab)
        #self.vocabulary.sort()
        #self.corpus_size = corpus_size
        #self.path = open((deva_path + "/docWeights.bin"),"rb")
        #self.connection = sqlite3.connect("bytepositions.db") not sure if i need this
        #self.path = open(deva_path,"rb")
        self.path = deva_path   # not sure which one i should use yet need to run it
    def get_postings(self, term : str) -> Iterable[Posting]:
        connection = sqlite3.connect(self.path / "bytepositions.db")
        preta_path = self.path / "postings.bin" # moves the path to the postings file
        f = open(preta_path,"rb")
        cursor = connection.cursor()
        cursor.execute("SELECT position FROM bytes WHERE terms = (?)", (term, ))
        for row in cursor:
            print(row)
        target_byte = cursor.fetchone()
        
        f.seek(target_byte[0]) # seek to the target_byte given by the query
        asc = f.read(4)
        size = struct.unpack('i', asc)[0]   # DFt
        print(size)
                                        # it will be read as a binary number and we need to set it to int
        posting_list = [None] * size # posting list we will return
        prev_docid = 0
        for s in size:  # for each doc containing the term
            f.seek(1,1) # seek to doc_id
            doc_id = struct.unpack('i', f.read(1)) #doc_id
            post = Posting(doc_id + prev_docid) #create a posting with the doc_id
            prev_docid = doc_id
            f.seek(1,1) # seek to tftd (number of positions)
            position_count = struct.unpack('i', f.read(1))
            prev_position = 0
            for t in position_count:
                f.seek(1,1) # seek to pi, (position of term in doc_id)
                position = struct.unpack('i', f.read(1))
                post.add_position(position + prev_position)
                prev_position = position
            posting_list.append(post)
        return posting_list
    #def add_term(self, term : str, doc_id : int):

    def get_no_postings(self, term: str) -> Iterable[Posting]:
        connection = sqlite3.connect(self.path / "bytepositions.db")
        cursor = connection.cursor()
        preta_path = self.path / "postings.bin" # moves the path to the postings file
        target_byte = cursor.execute("SELECT position FROM bytes WHERE terms = (?)", term)
        preta_path.seek(target_byte) # seek to the target_byte given by the query
        posting_list = [None] * size # posting list we will return
        size = int(preta_path.read(1))   # DFt
        prev_docid = 0
        for s in size:  # for each doc containing the term
            preta_path.seek(1,1) # seek to doc_id
            doc_id = struct.unpack('i', preta_path.read(1)) #doc_id
            post = Posting(doc_id + prev_docid) #create a posting with the doc_id
            prev_docid = doc_id
            posting_list.append(post)
        return posting_list

    def vocabulary(self) -> Iterable[str]:
        return self.vocabulary