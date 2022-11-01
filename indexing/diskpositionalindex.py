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
        self.connection = sqlite3.connect("bytepositions.db")
        self.path = deva_path
    def get_postings(self, term : str) -> Iterable[Posting]:
        connection = sqlite3.connect("bytepositions.db")
        cursor = connection.cursor()
        target_byte = 
    def add_term(self, term : str, doc_id : int):
    def vocabulary(self) -> Iterable[str]:
        return self.vocabulary