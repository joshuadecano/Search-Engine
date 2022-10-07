from .tokenprocessor import TokenProcessor
from typing import Iterable
import re
from porter2stemmer import Porter2Stemmer

class ProTokenProcessor(TokenProcessor):
    """A BasicTokenProcessor creates terms from tokens by removing all non-alphanumeric characters 
    from the token, and converting it to all lowercase."""
    whitespace_re = re.compile(r"\W+")

    def process_token(self, token : str) -> Iterable[str]:      # Now we will be returning a list of strings, 
        final_return = []                                       # (explains why hewlettpackardcomputing, hewlett, packard, and computing have the same position #)
        try:
            stemmer = Porter2Stemmer()
            temp = re.sub(self.whitespace_re, "", token).lower()    
            if not temp[0].isalnum():   # removes the first letter if its not alphanumeric
                temp = temp[1:]
            if not temp[-1].isalnum():  # removes the last letter if its not alphanumeric
                temp = temp[:-1]
            re.sub("'","", temp)    # removes apostrophes
            re.sub('"',"",temp)     # removes quotation marks
            stemmer.stem(temp)
            if '-' in temp:
                for t in temp.split("-"):
                    tok = t.strip()
                    if len(tok) > 0:
                        final_return.append(tok)
            else:
                final_return.append(temp)
        except:
            print("Exception: Index out of range")
        return final_return
