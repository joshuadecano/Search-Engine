from indexing import Index, PositionalInvertedIndex
from pathlib import Path
from bplustree import BPlusTree
import struct
import sqlite3
import os
import numpy as np

class DiskIndexWriter(Index):
    def write_index(self, pi : PositionalInvertedIndex, deva_path : Path, weights : list[float]):
        
        asura_path = deva_path / "postings.bin"
        if os.path.exists(asura_path) == True:
            os.remove(asura_path)
        f = open(asura_path,"wb")
        vocab = pi.vocabulary()
        connection = sqlite3.connect("bytepositions.db")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS bytes")
        cursor.execute("CREATE TABLE bytes (terms TEXT, position INTEGER)")
        print("vocab word to search: ", vocab[7])
        print(len(vocab))
        count = 0
        for s in vocab: #for each term in vocab
            prev_docid = 0
            if count == 7:
                print("byte location: ", f.tell())
                print("term: ", s)
                count +=1
            else:
                count +=1
            post = pi.get_postings(s)   # get postings list for each term
            
            position = f.tell() # DFT
            f.write(struct.pack('i', len(post)))    #dft
            for t in post:  # for each posting with term s
                f.write(struct.pack('i', (t.doc_id - prev_docid)))  #id
                tftd = len(t.position)
                wdt = float(1 + np.log(tftd))
                f.write(struct.pack('d', (wdt)))
                f.write(struct.pack('i', tftd))  #tftd
                prev_docid = t.doc_id        # stores the current doc_id for the gap
                prev_position = 0
                for u in t.position:
                    f.write(struct.pack('i', (u - prev_position)))  #pi
                    prev_position = u   # stores the current position for the gap
            terms = s
            inputs = (terms, position)
            add_byte_position = ("INSERT INTO bytes "
                                "(terms, position) "    # previous said %(term)s , %(position)s below 
                                "VALUES (?, ?)") #, (terms, position))
            cursor.execute(add_byte_position, inputs)
            connection.commit()
        connection.close()
        f.close()
        preta_path = deva_path / "docWeights.bin"
        g = open(preta_path,"wb")
        for x in weights:
            g.write(struct.pack('d', x))
        g.close()