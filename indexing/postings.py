class Posting:
    """A Posting encapulates a document ID associated with a search query component."""
    def __init__(self, doc_id : int):
        self.doc_id = doc_id
        self.position = []
        self.dft = 0
    def add_position(self, position : int):
        return self.position.append(position)