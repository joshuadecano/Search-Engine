from indexing.postings import Posting
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    def __init__(self, terms : list[str]):
        self.terms = [s for s in terms]

    def get_postings(self, index) -> list[Posting]:
        for s in self.terms:
            return terms
        return None
        # positional merge: first check for doc ids that all of the postings share, next 
        # basically two for loops 
        # TODO: program this method. Retrieve the postings for the individual terms in the phrase,
		# and positional merge them together.

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'