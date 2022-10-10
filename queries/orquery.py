from .querycomponent import QueryComponent
from indexing import Index, Posting

from queries import querycomponent 

class OrQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        result = []
        result.append(self.components[0])
        count = 0
        num = len(self.components)     # number of terms in AND query
        while count < num:
            #for s in self.components:
            result.append(self.intersect(result, self.components[count+1]))
            count += 1
        return result
        
    def union(self, index : Index, p1 : QueryComponent, p2 : QueryComponent):
        answer = []
        inc1 = 0
        inc2 = 0
        post1 = p1.get_postings(Index)      # returns a list of postings
        post2 = p2.get_postings(Index)      # returns a list of postings
        while inc1 < len(p1.get_postings()) and inc2 < len(p2.get_postings()):
            if post1[inc1].doc_id == post2[inc2].doc_id:
                if answer[-1] == post1[inc1].doc_id:
                    continue # ? 
                else:
                    answer.append(post1[inc1].doc_id)
            elif post1[inc1].doc_id < post2[inc2].doc_id:
                answer.append(post1[inc1].doc_id)
                inc1 += 1
            else:
                answer.append(post2[inc2].doc_id)
                inc2 += 1
        return answer


    def __str__(self):
        return "(" + " OR ".join(map(str, self.components)) + ")"