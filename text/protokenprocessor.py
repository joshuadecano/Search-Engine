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
        stemmer = Porter2Stemmer()
        token.lower()
        #temp = re.sub(self.whitespace_re, "", token).lower()
        while token != "":                  # while the term is not empty
            while not token[0].isalnum():   # removes the first letter if its not alphanumeric
                token = token[1:]
            while not token[-1].isalnum():  # removes the last letter if its not alphanumeric
                token = token[:-1]
        if token == "":
            return None
        re.sub("'","", token)    # removes apostrophes
        re.sub('"',"",token)     # removes quotation marks
        stemd = stemmer.stem(token)
        if '-' in stemd:
            for t in token.split("-"):
                tok = t.strip()
                if len(tok) > 0:
                    final_return.append(tok)
        else:
            final_return.append(stemd)
        #except:
        #    nothings = 0
        return final_return
