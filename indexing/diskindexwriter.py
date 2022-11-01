from indexing import Index, PositionalInvertedIndex
from pathlib import Path
import struct
import sqlite3
def write_index(pi : PositionalInvertedIndex, deva_path : Path):
    asura_path = deva_path + "postings.bin"
    f = open(asura_path,"rb")
    vocab = pi.vocabulary()
    connection = sqlite3.connect("bytepositions.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE bytes (position INTEGER)")
    add_byte_position = ("INSERT INTO bytes "
                        "(position) "
                        "VALUES (%(position)s)")
    for s in vocab:
        post = pi.get_postings(s)
        f.write(struct.pack(len(post)))
        prev_docid = 0
        for t in post:
            f.write(struct.pack(t.doc_id - prev_docid))
            f.write(struct.pack(len(t.position)))
            prev_docid = post[t]        # stores the current doc_id for the gap
            prev_position = 0
            for u in t.position:
                f.write(struct.pack(u - prev_position))
                prev_position = u   # stores the current position for the gap
        f.seek(len(post))
        inputs = {
            'position': f.tell()
        }
        cursor.execute(add_byte_position, inputs)