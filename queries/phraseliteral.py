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
        #need to change this to a while statement where while counter < len(p_list1) and counter < len(p_list2)
        counter1 = 0
        counter2 = 0
        while counter1 < p_list1 and counter2 < p_list2:
            if p_list1[counter1].doc_id == p_list2[counter2].doc_id:
                post = Posting(p_list1[counter1].doc_id)
                pp1 = []
                pp2 = []
                pp1 = p_list1[counter1].position
                pp2 = p_list2[counter2].position
                positions = self.position_compare(index,pp1,pp2,k)
                counter1 += 1
                counter2 += 1
                if positions:   # if position_compare succeeds
                    post.add_position(positions)
                    new_posting_list.append(post)
                else:
                    continue
                #### I'm not sure if .doc_id is ordered, so i need to test this
            elif p_list1[counter1].doc_id < p_list2[counter2].doc_id:
                counter1 += 1
            else:
                counter2 += 1
        return new_posting_list

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'
