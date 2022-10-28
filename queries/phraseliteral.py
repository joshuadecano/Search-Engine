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
        answer = index.get_postings(self.terms[0])
        comparisons = len(self.terms) - 1        # amount of comparisons we will need

        for s in range(comparisons):
            list2 = index.get_postings(self.terms[s+1])
            answer = self.positional_intersect(index, answer, list2, s+1)

        return answer

    def position_compare(self, index : Index, p1 : list[int], p2 : list[int], k : int) -> list[int]:            #checks the posting positions
        result = []
        for a in p1:
            for b in p2:
                if a and b is not None:
                    if abs(a-b) == k:
                        result.append(a)
                        return a
                    else:
                        continue
        #return result

    def positional_intersect(self, index : Index, p_list1: list[Posting], p_list2: list[Posting], k : int) -> list[Posting]:        # ANDs postings of both lists
        new_posting_list = []
        for s in p_list1:
            for t in p_list2:
                if s.doc_id == t.doc_id:
                    post = Posting(s.doc_id)
                    pp1 = []
                    pp2 = []
                    pp1 = s.position
                    pp2 = t.position
                    positions = self.position_compare(index,pp1,pp2,k)
                    if positions:
                        post.add_position(positions)
                        new_posting_list.append(post)
                    else:
                        continue
        return new_posting_list

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'
