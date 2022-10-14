#from asyncio.windows_events import NULL
#from os import terminal_size
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
        print(self.terms)
        print(answer)
        term_count = len(self.terms)        # number of terms in phrase literal
        comparisons = term_count - 1        # amount of comparisons we will need
        for s in range(comparisons):        # for each comparison
            self.pos_match(index, answer, self.terms[s+1], s+1)
        return answer
    def doc_match(self, index, term1 : str, term2 : str) -> list[int]:
        doc_list = []                             # holds the list for document IDs
        posting_list2 = []
        posted = []
        
        list1 = index.get_postings(term1)       # gets the postings for term1
        #print(list1)
        list2 = index.get_postings(term2)
        for s in list1:
            for t in list2:
                if s.doc_id == t.doc_id:
                    doc_list.append(s.doc_id)       # holds the document IDs where both terms appear
        return doc_list
    
    def pos_match(self, index, term1 : str, term2 : str, k : int):      # takes in the index, first and second term, and gap (k)
        #print(term1)
        #print(term2)
        doc_list = self.doc_match(index, term1, term2)                  
        second_list = []    # holds the list for positions
        list1 = index.get_postings(term1)                       # list of postings
        list2 = index.get_postings(term2)                       # list of postings
        for s in doc_list:                 # for each document id stored                 
            for t in list1:                # for each posting for a given term
                #if t.doc
                #
                #
                for u in list2:
                    while t.doc_id == s:
                        if (t.position[s] - k) == u.position:       # changed to t.position[s] because the S will be the doc_id, need to check what it returns
                            second_list.append(s.position)
        return second_list

        # TODO: program this method. Retrieve the postings for the individual terms in the phrase,
		# and positional merge them together.

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'