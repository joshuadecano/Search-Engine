from asyncio.windows_events import NULL
from indexing.postings import Posting
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    def __init__(self, terms : list[str]):
        self.terms = [s for s in terms]

    def get_postings(self, index) -> list[Posting]:
        terms_holder = []
        answer = []
        term_length = range(self.terms)
        i = 1
        for s in self.terms:
            terms_holder[s] = index.get_postings(s)
        while i < term_length:          # while the index of the second term(starts at index 1) is less than the length of the phrase
            while terms_holder[i-1] != NULL and terms_holder[i] != NULL:
                if terms_holder[i-1].doc_id == terms_holder[i].doc_id:
                    l = []
                    pp1 = terms_holder[i-1]
                    pp2 = terms_holder[i]
                    while pp1 != NULL:
                        while pp2 != NULL:
                            if (pp1.position[] - pp2.position

                    
        ##### BIGGEST HELP IS GONNA BE ON RECORDED LECTURE DAY 4 AT AROUND 29:20
        ##### code in textbook is on page 42
        # if 
        # positional merge: first check for doc ids that all of the postings share, next 
        # TODO: program this method. Retrieve the postings for the individual terms in the phrase,
		# and positional merge them together.

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'