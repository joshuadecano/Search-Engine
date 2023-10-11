from .index import Index
from typing import Iterable
from indexing.postings import Posting
from pathlib import Path
import struct
import sqlite3

class DiskPositionalIndex(Index):
    def __init__(self, deva_path: Path): # I took out ", vocab : Iterable[str], corpus_size : int" because i dont think we need it
        self.path = deva_path
        self.vocabular = []

    def get_postings(self, term : str) -> Iterable[Posting]:
        connection = sqlite3.connect("bytepositions.db")
        preta_path = self.path / "postings.bin" # moves the path to the postings file
        f = open(preta_path,"rb")
        cursor = connection.cursor()
        cursor.execute("SELECT position FROM bytes WHERE terms = (?)", (term, ))
        target_byte = cursor.fetchone()
        f.seek(target_byte[0]) # seek to the target_byte given by the query
        size = struct.unpack('i', f.read(4))[0]   # DFt document frequency
        if term not in self.vocabular:
            self.vocabular.append(term)
        posting_list = []
        prev_docid = 0
        for s in range(size):  # for each doc containing the term
            doc_id = struct.unpack('i', f.read(4))[0] #doc_id
            post = Posting(doc_id + prev_docid) #create a posting with the doc_id
            prev_docid += doc_id
            position_count = struct.unpack('i', f.read(4))[0]
            prev_position = 0
            for t in range(position_count):
                position = struct.unpack('i', f.read(4))[0]
                post.add_position(position + prev_position)
                prev_position += position
            post.dft = size
            posting_list.append(post)
        return posting_list

    def get_no_postings(self, term: str) -> Iterable[Posting]:
        connection = sqlite3.connect(self.path / "bytepositions.db")
        cursor = connection.cursor()
        preta_path = self.path / "postings.bin" # moves the path to the postings file
        f = open(preta_path,"rb")
        cursor.execute("SELECT position FROM bytes WHERE terms = (?)", (term, ))
        target_byte = cursor.fetchone()
        f.seek(target_byte[0]) # seek to the target_byte given by the query
        posting_list = [] # posting list we will return
        size = struct.unpack('i', f.read(4))[0]   # DFt
        prev_docid = 0
        for s in range(size):  # for each doc containing the term
            doc_id = struct.unpack('i', f.read(4))[0] #doc_id
            f.seek(8,1) # skips past the wdt since it isn't important here
            post = Posting(doc_id + prev_docid) #create a posting with the doc_id
            prev_docid += doc_id
            posting_list.append(post)
            tftd = struct.unpack('i', f.read(4))[0]       # tftd, using it to jump this many bytes ahead
            f.seek(tftd * 4,1)
        return posting_list

    def vocabulary(self) -> Iterable[str]:
        return self.vocabular