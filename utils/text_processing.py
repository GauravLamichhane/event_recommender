import re
from typing import List, Set

class TextProcessor:
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 
            'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 
            'with', 'this', 'but', 'they', 'have', 'had', 'what', 'said', 'each', 
            'which', 'do', 'how', 'their', 'if', 'up', 'out', 'many', 'then', 'them',
            'or', 'so', 'can', 'all', 'any', 'get', 'use', 'now', 'way', 'may', 'say',
            'come', 'could', 'see', 'time', 'very', 'when', 'much', 'go', 'well', 
            'little', 'good', 'make', 'world', 'over', 'think', 'also', 'back', 
            'after', 'first', 'work', 'life'
        }
    
    def preprocess_text(self, text: str) -> List[str]:
        if not text:
            return []
        
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        tokens = text.split()
        
        return [token for token in tokens 
                if token not in self.stop_words and len(token) > 2 and token.isalpha()]
    
    def get_vocabulary(self, documents: List[str]) -> Set[str]:
        vocab = set()
        for doc in documents:
            if doc:
                vocab.update(self.preprocess_text(doc))
        return vocab
