from indexing import Index, PositionalInvertedIndex
from pathlib import Path
import struct
import sqlite3
import os

class DiskIndexWriter(Index):
    def write_index(self, pi : PositionalInvertedIndex, deva_path : Path, weights : list[float]):
        asura_path = deva_path / "postings.bin"
        os.remove(asura_path)
        f = open(asura_path,"wb")
        vocab = pi.vocabulary()
        connection = sqlite3.connect("bytepositions.db")
        connection.close()
        connection = sqlite3.connect("bytepositions.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE bytes (terms TEXT, position INTEGER)")
        add_byte_position = ("INSERT INTO bytes "
                            "(terms, position) "
                            "VALUES (%(term)s ,%(position)s)")
        for s in vocab: #for each term in vocab
            post = pi.get_postings(s)   # get postings list for each term
            f.write(struct.pack('i', len(post)))    #dft
            prev_docid = 0  
            for t in post:  # for each posting with term s
                f.write(struct.pack('i', (t.doc_id - prev_docid)))  #id
                f.write(struct.pack('i', len(t.position)))  #tftd
                prev_docid = t.doc_id        # stores the current doc_id for the gap
                prev_position = 0
                for u in t.position:
                    f.write(struct.pack('i', (u - prev_position)))  #pi
                    prev_position = u   # stores the current position for the gap
            f.seek(len(post))   
            inputs = {
                'terms' : s,
                'position': f.tell()
            }    
            f.seek(0,2) #move the file pointer to the end of a file
            cursor.execute(add_byte_position, inputs)
        connection.close()
        f.close()
        preta_path = deva_path / "docWeights.bin"
        g = open(preta_path,"wb")
        for x in weights:
            g.write(struct.pack('d', x))
        g.close()