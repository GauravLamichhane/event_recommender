import re
import math
from typing import List, Dict, Set
from collections import Counter

class TextProcessor:
    def __init__(self):
        # Common English stop words
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 
            'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 
            'that', 'the', 'to', 'was', 'will', 'with', 'the', 'this',
            'but', 'they', 'have', 'had', 'what', 'said', 'each', 'which',
            'do', 'how', 'their', 'if', 'up', 'out', 'many', 'then', 'them',
            'or', 'so', 'can', 'all', 'any', 'get', 'use', 'now', 'way',
            'may', 'say', 'come', 'could', 'see', 'time', 'very', 'when',
            'much', 'go', 'well', 'little', 'good', 'make', 'world', 'over',
            'think', 'also', 'back', 'after', 'first', 'work', 'life'
        }
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text by converting to lowercase, removing punctuation,
        tokenizing, and removing stop words.
        """
        if not text:
            return []
        
        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        
        # Tokenize by splitting on whitespace
        tokens = text.split()
        
        # Remove stop words and short tokens (less than 3 characters)
        filtered_tokens = []
        for token in tokens:
            if (token not in self.stop_words and 
                len(token) > 2 and 
                token.isalpha()):  # Only keep alphabetic tokens
                filtered_tokens.append(token)
        
        return filtered_tokens
    
    def get_vocabulary(self, documents: List[str]) -> Set[str]:
        """Get unique vocabulary from all documents."""
        vocab = set()
        for doc in documents:
            if doc:  # Check if document is not empty
                tokens = self.preprocess_text(doc)
                vocab.update(tokens)
        return vocab
    
    def get_document_frequency(self, documents: List[str]) -> Dict[str, int]:
        """Get document frequency for each term in the vocabulary."""
        doc_freq = {}
        vocab = self.get_vocabulary(documents)
        
        for term in vocab:
            doc_freq[term] = 0
            for doc in documents:
                if doc and term in self.preprocess_text(doc):
                    doc_freq[term] += 1
                    
        return doc_freq
