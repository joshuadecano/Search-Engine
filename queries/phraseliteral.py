#from asyncio.windows_events import NULL
#from os import terminal_size
from indexing import Index
from indexing.postings import Posting
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    def __init__(self, terms : list[str]):
        self.terms = [s for s in terms]

    def get_postings(self, index : Index) -> list[Posting]:
        answer = []
        print("called")
        print(self.terms)
        answer = index.get_postings(self.terms[0])
        #answer.append(index.get_postings(self.terms[0]))       # starting off with the first term
        print("answer = ", answer)
        #print(type(answer))
        print("self.terms = ", self.terms[0])
        #term_count = len(self.terms)        # number of terms in phrase literal
        comparisons = len(self.terms) - 1        # amount of comparisons we will need
        #print(comparisons)
        for s in range(comparisons):        # for each comparison       
            #list1 = index.get_postings(answer[0])      
            list2 = index.get_postings(self.terms[s+1])
##            for s in list1:
##                for t in list2:
##                    if s.doc_id == t.doc_id:
##                        pp1 = []                    #list to hold positions
##                        pp2 = []                    #list to hold positions
##                        pp1.append(s.position)
##                        pp2.append(t.position)
                        #ell = []
                        #ell = s.position            # holds a list of positions for term1
                        #pp2 = t.position            # holds a list of positions for term2
                        #ell = self.position_compare(index, ell, pp2, s+1)
            #next_one = []
            #next_one.append(self.terms[s+1])
            answer = self.positional_intersect(index, answer, list2, s+1)

        return answer

    def position_compare(self, index : Index, p1 : list[int], p2 : list[int], k : int) -> list[int]:            #checks the posting positions
        result = []
        for a in p1:
            for b in p2:
                if a and b is not None:
                    if abs(a - b) <= k:         # got an error saying i cant subtract NoneType and int
                        result.append(a)
                        return a
                    elif b > a:
                        break
        #return result

    def positional_intersect(self, index : Index, p_list1: list[Posting], p_list2: list[Posting], k : int) -> list[Posting]:        # ANDs postings of both lists
        #list1 = index.get_postings(term1)
        #list2 = index.get_postings(term2)
        new_posting_list = []
        for s in p_list1:
            for t in p_list2:
                if s.doc_id == t.doc_id:
                    #if s.position and t.position is not None:
                    post = Posting(s.doc_id)
                    pp1 = []
                    pp2 = []
                    pp1 = s.position
                    pp2 = t.position
                    positions = self.position_compare(index,pp1,pp2,k)
                    post.add_position(positions)
                    new_posting_list.append(post)
                    #ell = []
                    #pp1 = s.position            # holds a list of positions for term1
                    #pp2 = t.position            # holds a list of positions for term2
                    #new_posting_list.append(self.position_compare(index, pp1, pp2, k))
        return new_posting_list





    
##    def doc_match(self, index, term1 : str, term2 : str) -> list[int]:
##        doc_list = []                             # holds the list for document IDs
##        posting_list2 = []
##        posted = []
##        
##        list1 = index.get_postings(term1)       # gets the postings for term1
##        #print(list1)
##        list2 = index.get_postings(term2)
##        for s in list1:
##            for t in list2:
##                if s.doc_id == t.doc_id:
##                    doc_list.append(s.doc_id)       # holds the document IDs where both terms appear
##        return doc_list
##    
##    def pos_match(self, index, term1 : str, term2 : str, k : int):      # takes in the index, first and second term, and gap (k)
##        #print(term1)
##        #print(term2)
##        doc_list = self.doc_match(index, term1, term2)                  
##        second_list = []    # holds the list for positions
##        list1 = index.get_postings(term1)                       # list of postings
##        list2 = index.get_postings(term2)                       # list of postings      
##        for s in doc_list:                 # for each document id stored                 
##            for t in list1:                # for each posting for a given term
##                for z in t.position:
##                    while t.doc_id == s:
##                        if (z - k) == 
##                #if t.doc
##                #
##                #                                      # list1 = postings objects (also has doc_id and position)
##                for u in list2:                        # t = posting objects(has doc_id and position), to get position, t.position
##                    while t.doc_id == s:               # s = doc_ids (49,20) 
##                        if (t.position[s] - k) == u.position:       # changed to t.position[s] because the S will be the doc_id, need to check what it returns
##                            second_list.append(s.position)
##        return second_list

        # TODO: program this method. Retrieve the postings for the individual terms in the phrase,
		# and positional merge them together.

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'
