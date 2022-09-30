from pathlib import Path
from typing import Iterable
from .document import Document
from io import StringIO
import json
class JsonFileDocument(Document):
    """
    Represents a document that is saved as a simple text file in the local file system.
    """
    def __init__(self, id : int, path : Path):
        super().__init__(id)
        
        self.path = path

    @property
    def title(self) -> str:
        with open(self.path, 'r', encoding="utf-8") as file:
            jtitle = json.load(file)
            self.title = jtitle["title"]
            return self.title

    # returns TextIOWrapper
    def get_content(self) -> Iterable[str]:
        with open(self.path, 'r',encoding="utf-8") as file:
            jstring = json.load(file)
            nealdt = StringIO(jstring["body"])
            return nealdt

    @staticmethod
    def load_from(abs_path : Path, doc_id : int) -> 'JsonFileDocument' :
        """A factory method to create a TextFileDocument around the given file path."""
        return JsonFileDocument(doc_id, abs_path)
