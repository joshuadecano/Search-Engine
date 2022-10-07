from asyncio.windows_events import NULL
from os import terminal_size
from indexing.postings import Posting
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    def __init__(self, terms : list[str]):
        self.terms = [s for s in terms]

    def get_postings(self, index) -> list[Posting]:
        answer = []
        answer = self.terms[0]              # starting off with the first term
        term_count = range(self.terms)
        comparisons = term_count - 2
        for s in range(comparisons):
            diff = s + 1
            self.pos_match(index, answer, self.term[diff], diff)

        return answer

        return 0
    #    for s in self.terms:
    #        terms_holder[s] = index.get_postings(s)
    #    while i < term_length:          # while the index of the second term(starts at index 1) is less than the length of the phrase
    #        while terms_holder[i-1] != NULL and terms_holder[i] != NULL:
    #            if terms_holder[i-1].doc_id == terms_holder[i].doc_id:
    #                l = []
    #                pp1 = terms_holder[i-1]
    #                pp2 = terms_holder[i]
    #                while pp1 != NULL:
    #                    while pp2 != NULL:
    #                        if (pp1.position[] - pp2.position
    def doc_match(self, index, term1 : str, term2 : str) -> list[int]:
        doc_list = []
        posting_list2 = []
        posted = []
        list1 = index.get_postings(term1)
        list2 = index.get_postings(term2)
        for s in list1:
            for t in list2:
                if s.doc_id == t.doc_id:
                    doc_list.append(s.doc_id)       # holds the document IDs where both terms appear
        return doc_list
    
    def pos_match(self, index, term1 : str, term2 : str, k : int):
        doc_list = self.doc_match(index, term1, term2)
        second_list = []
        list1 = index.get_postings(term1)
        list2 = index.get_postings(term2)
        for s in doc_list:                      
            for t in list1:
                for u in list2:
                    while t.doc_id == s:
                        if (t.position - k) == u.position:
                            second_list.append(s.position)
        return second_list

        # have one function locating two documents that match and pass off their posting list to another helping list that does the positions themselves.
        ##### BIGGEST HELP IS GONNA BE ON RECORDED LECTURE DAY 4 AT AROUND 29:20
        ##### code in textbook is on page 42
        # if 
        # positional merge: first check for doc ids that all of the postings share, next 
        # TODO: program this method. Retrieve the postings for the individual terms in the phrase,
		# and positional merge them together.

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'