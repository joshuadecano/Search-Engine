from .tokenprocessor import TokenProcessor
from typing import Iterable
import re
from porter2stemmer import Porter2Stemmer

class ProTokenProcessor(TokenProcessor):
    """A BasicTokenProcessor creates terms from tokens by removing all non-alphanumeric characters 
    from the token, and converting it to all lowercase."""
    whitespace_re = re.compile(r"\W+")

    def process_token(self, token : str) -> Iterable[str]:      # Now we will be returning a list of strings,
        final_return = []                                     # (explains why hewlettpackardcomputing, hewlett, packard, and computing have the same position #)
        stemmer = Porter2Stemmer()
##  I need to split a string like "fires in yosemite" to "fires" "in" "yosemite"
        #temp = re.sub(self.whitespace_re, "", token).lower()
        while token != "":                  # while the term is not empty
            if not token[0].isalnum():   # removes the first letter if its not alphanumeric
                token = token[1:]
                if token == "":
                    break
            if not token[-1].isalnum():  # removes the last letter if its not alphanumeric
                token = token[:-1]
                if token == "":
                    break
            if token[0].isalnum() and token[-1].isalnum():
                break
        if token == "":
            return None
        atoken = re.sub("'","", token)    # removes apostrophes
        qtoken = re.sub('"',"",atoken)     # removes quotation marks
        if '-' in qtoken:
            for t in qtoken.split("-"):
                tok = t.strip()
                if len(tok) > 0:
                    stemd = stemmer.stem(tok)
                    final_return.append(stemd)
        #ltoken = token.lower()
        stemd = stemmer.stem(qtoken)
        final_return.append(stemd)
        #except:
        #    nothings = 0
        return final_return
