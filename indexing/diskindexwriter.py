from indexing import Index, PositionalInvertedIndex
from pathlib import Path
import struct
def write_index(pi = PositionalInvertedIndex):
    f = open("postings.bin","wb")
    vocab = pi.vocabulary()
    for s in vocab:
        post = pi.get_postings(s)
