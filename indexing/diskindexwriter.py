from indexing import Index, PositionalInvertedIndex
from pathlib import Path
import struct
import sqlite3
def write_index(pi : PositionalInvertedIndex):
    f = open("postings.bin","wb")
    vocab = pi.vocabulary()
    connection = sqlite3.connect("")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE bytes (position INTEGER)")
    add_byte_position = ("INSERT INTO bytes "
                        "(position) "
                        "VALUES (%(position)s)")
    for s in vocab:
        post = pi.get_postings(s)
        f.write(struct.pack(len(post)))
        for t in post:
            f.write(struct.pack(t.doc_id))
            f.write(struct.pack(len(t.position)))
            for u in t.position:
                f.write(struct.pack(u))
        f.seek(len(post))
        inputs = {
            'position': f.tell()
        }
        cursor.execute(add_byte_position, inputs)