from .querycomponent import QueryComponent
from indexing import Index, Posting

from queries import querycomponent 

class AndQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        result = []
        result = self.components[0]
        count = 0
        num = range(self.components)     # number of terms in AND query
        result = self.components[0]
        while count < num:
            #for s in self.components:
            result.append(self.intersect(result, self.components[count+1]))
            count += 1
        return result
    def intersect(self, p1 : QueryComponent, p2 : QueryComponent):
        answer = []
        inc1 = 0
        inc2 = 0
        while inc1 < range(p1) and inc2 < range(p2):
            if p1.get_postings[inc1].doc_id == p2.get_postings[inc2].doc_id:
                answer.append(p1.get_postings.doc_id)
            elif p1.get_postings[inc1].doc_id < p2.get_postings[inc2].doc_id:
                inc1 += 1
            else:
                inc2 += 1
        return answer
        # TODO: program the merge for an AndQuery, by gathering the postings of the composed QueryComponents and
		# intersecting the resulting postings.
        #return result

    def __str__(self):
        return " AND ".join(map(str, self.components))