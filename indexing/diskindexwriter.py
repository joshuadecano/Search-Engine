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
        cursor.execute("DROP TABLE IF EXISTS bytes")
        cursor.execute("CREATE TABLE bytes (terms TEXT, position INTEGER)")
        print("vocab word to search: ", vocab[7])
        print(len(vocab))
        count = 1
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
                f.write(struct.pack('i', len(t.position)))  #tftd
                prev_docid = t.doc_id        # stores the current doc_id for the gap
                prev_position = 0
                for u in t.position:
                    f.write(struct.pack('i', (u - prev_position)))  #pi
                    prev_position = u   # stores the current position for the gap
            #f.seek(len(post))   
            #inputs = {
            #    'terms' : s,
            #    'position': f.tell()
            #}  
            
            terms = s
            #position = f.tell()
            inputs = (terms, position)
            #f.seek(0,2) #move the file pointer to the end of a file
            add_byte_position = ("INSERT INTO bytes "
                                "(terms, position) "    # previous said %(term)s , %(position)s below 
                                "VALUES (?, ?)") #, (terms, position))
            cursor.execute(add_byte_position, inputs)
            connection.commit()
        print("jesus christ")
        connection.close()
        f.close()
        preta_path = deva_path / "docWeights.bin"
        g = open(preta_path,"wb")
        for x in weights:
            g.write(struct.pack('d', x))
        g.close()