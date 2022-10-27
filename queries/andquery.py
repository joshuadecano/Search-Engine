from .querycomponent import QueryComponent
from indexing import Index, Posting

from queries import QueryComponent 

class AndQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        #result = []
        print("what am i doing here")
        result = self.components[0].get_postings(index)      # starts the list off with the first (term literal) object
                                                # but this isnt right, it should just be a list of lists of postings
        count = 0
        num = len(self.components)     # number of terms in AND query
        while count < num-1:
            #p1 = self.components[count].get_postings(index)
            p2 = self.components[count+1].get_postings(index)
            result = self.intersect(result, p2)
            
            count += 1
        return result
    def intersect(self, post1: list[Posting] , post2 : list[Posting]) -> list[Posting]: 
        answer = []
        #post1 = p1.get_postings(index)      # returns a list of postings
        #post2 = p2.get_postings(index)      # returns a list of postings
        #print(len(post1))
        #print(len(post2))           # floral rock works but rock floral does not.. wtf???
        inc1 = 0
        inc2 = 0
        if post1 and post2 is not None:
            while inc1 < len(post1) and inc2 < len(post2):
            #while len(post1) >= 0 and len(post2) >= 0:
            # got an error saying object of nonetype has no len()
            # probably have to do a try catch here? or go back and see why 
            #while p1 and p2:
                if post1[inc1].doc_id == post2[inc2].doc_id:
                #if p1.get_postings[inc1].doc_id == p2.get_postings[inc2].doc_id:
                    answer.append(post1[inc1])
                    inc1 += 1
                    inc2 += 1
                elif post1[inc1].doc_id < post2[inc2].doc_id:
                    inc1 += 1
                else:
                    inc2 += 1
        return answer
        # TODO: program the merge for an AndQuery, by gathering the postings of the composed QueryComponents and
		# intersecting the resulting postings.
        #return result

    def __str__(self):
        return " AND ".join(map(str, self.components))
