from .tokenprocessor import TokenProcessor
import re

class BasicTokenProcessor(TokenProcessor):
    """A BasicTokenProcessor creates terms from tokens by removing all non-alphanumeric characters 
    from the token, and converting it to all lowercase."""
    whitespace_re = re.compile(r"\W+")
    
    def process_token(self, token : str) -> str:
        temp = re.sub(self.whitespace_re, "", token).lower()
        if not temp[0].isalnum():   # removes the first letter if 
            temp = temp[1:]
        if not temp[-1].isalnum():
            temp = temp[:-1]
        re.sub("'","", temp)
        re.sub('"',"",temp)
        # not finished, I need to do the hyphen parts
        return temp
