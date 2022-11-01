from indexing import Index, PositionalInvertedIndex
from pathlib import Path
import struct
import sqlite3
import numpy as np
def write_index(pi : PositionalInvertedIndex, deva_path : Path):
    hashmap = {}
    asura_path = deva_path + "postings.bin"
    f = open(asura_path,"rb")
    vocab = pi.vocabulary()
    connection = sqlite3.connect("bytepositions.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE bytes (terms TEXT, position INTEGER)")
    add_byte_position = ("INSERT INTO bytes "
                        "(terms, position) "
                        "VALUES (%(term)s ,%(position)s)")
    for s in vocab: #for each term in vocab
        post = pi.get_postings(s)
        f.write(struct.pack('i', len(post)))
        prev_docid = 0
        occurences = 0
        for t in post:  # for each posting with term s
            f.write(struct.pack('i', (t.doc_id - prev_docid)))
            f.write(struct.pack('i', len(t.position)))
            prev_docid = post[t]        # stores the current doc_id for the gap
            prev_position = 0
            occurences = len(t.position)
            for u in t.position:
                f.write(struct.pack('i', (u - prev_position)))
                prev_position = u   # stores the current position for the gap

            hashmap[s] = occurences     # key = term, value = tftd
            preta_path = deva_path + "docWeights.bin"
            g = open(preta_path,"rb")
            g.write(struct.pack('d', ld))
            
        f.seek(len(post))   
        inputs = {
            'terms' : s,
            'position': f.tell()
        }    
        f.seek(0,2) #move the file pointer to the end of a file
        cursor.execute(add_byte_position, inputs)
