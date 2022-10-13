from .querycomponent import QueryComponent
from indexing import Index, Posting

from queries import QueryComponent 

class OrQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        #result = []
        result = self.components[0].get_postings(index)  
        count = 0
        num = len(self.components)     # number of terms in AND query
        while count < num - 1:
            #for s in self.components:
            p2 = self.components[count+1].get_postings(index)
            result = self.union(result, p2)
            count += 1
        return result
        
    def union(self, post1: list[Posting] , post2 : list[Posting]) -> list[Posting]:
        answer = []
        inc1 = 0
        inc2 = 0
        #post1 = p1.get_postings(index)      # returns a list of postings
        #post2 = p2.get_postings(index)      # returns a list of postings
        # Recently this showed up as out of range, not sure if this fixed it
        # before it was while p1 and p2:
        while inc1 < len(post1) and inc2 < len(post2):
            if post1[inc1].doc_id == post2[inc2].doc_id:
                if answer[-1] == post1[inc1].doc_id:    # if the most recently added posting matches the current doc_id:
                    break # ?
                else:
                    answer.append(post1[inc1])
                    inc1 += 1
                    inc2 += 1
            elif post1[inc1].doc_id < post2[inc2].doc_id:
                answer.append(post1[inc1])
                inc1 += 1
            elif post1[inc1].doc_id > post2[inc2].doc_id:
                answer.append(post2[inc2])
                inc2 += 1
        while inc1 == len(post1) and inc2 < len(post2):
            answer.append(post2[inc2])
            inc2 += 1
        while inc2 == len(post2) and inc1 < len(post1):
            answer.append(post1[inc1])
            inc1 += 1            
        return answer


    def __str__(self):
        return "(" + " OR ".join(map(str, self.components)) + ")"