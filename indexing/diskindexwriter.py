from indexing import Index, PositionalInvertedIndex
from pathlib import Path
import struct
#import math
import sqlite3
#import numpy as np

class DiskIndexWriter(Index):
    def write_index(pi : PositionalInvertedIndex, deva_path : Path, weights : list[float]):
        hashmap = {}
        anomap = {} # key : doc_id, value : term
        asura_path = deva_path + "/postings.bin"
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
            f.write(struct.pack('i', len(post)))    #dft
            prev_docid = 0
            occurrences = 0
            for t in post:  # for each posting with term s
                anomap[t.doc_id] = {}
                #anomap[t.doc_id].append(s)
                f.write(struct.pack('i', (t.doc_id - prev_docid)))  #id
                f.write(struct.pack('i', len(t.position)))  #tftd
                prev_docid = post[t]        # stores the current doc_id for the gap
                prev_position = 0
                occurrences = len(t.position)
                for u in t.position:
                    f.write(struct.pack('i', (u - prev_position)))  #pi
                    prev_position = u   # stores the current position for the gap
    #### begin thinking here (calculating document weights)
                #for c in pi.corpus_size:

                hashmap[s] = occurrences     # key = term, value = tftd
                anomap[t.doc_id] = hashmap[s]
                #preta_path = deva_path + "docWeights.bin"
                #g = open(preta_path,"rb")
                #g.write(struct.pack('d', ld))
    #### made a nested dictionary where key1 = term, key2 = doc_id, value = tftd
            f.seek(len(post))   
            inputs = {
                'terms' : s,
                'position': f.tell()
            }    
            f.seek(0,2) #move the file pointer to the end of a file
            cursor.execute(add_byte_position, inputs)
            
    #not sure if i need to close this
        f.close()
    #
        preta_path = deva_path + "/docWeights.bin"
        g = open(preta_path,"rb")
        for x in weights:
            g.write(struct.pack('d', x))
        g.close()
    #    for c in pi.corpus_size: # for each document
    #        sum = 0
    #        for d in anomap[c]:
    #            temp = (1 + np.log(d))
    #            sum += temp**2
    #        ld = math.sqrt(sum)
            
    #        g.write(struct.pack('d', ld))
    #    g.close()
    # to calculate document weights i need
    # a way to walk down the documents in order
    # a way to check to see if the term occurs in the document
    # need to know each term that occurs in document and its count
    # need to know 
