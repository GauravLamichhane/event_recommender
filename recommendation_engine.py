
import math
from typing import List, Dict, Tuple
from collections import Counter
from utils.text_processing import TextProcessor

class TFIDFRecommendationEngine:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.vocabulary = set()
        self.idf_scores = {}
        
    def calculate_tf(self, tokens: List[str]) -> Dict[str, float]:
        if not tokens:
            return {}
        token_count = Counter(tokens)
        doc_length = len(tokens)
        return {token: count / doc_length for token, count in token_count.items()}
    
    def calculate_idf(self, documents: List[str]) -> Dict[str, float]:
        total_documents = len(documents)
        if total_documents == 0:
            return {}
        
        self.vocabulary = self.text_processor.get_vocabulary(documents)
        term_doc_count = {}
        
        for term in self.vocabulary:
            term_doc_count[term] = sum(1 for doc in documents 
                                     if term in set(self.text_processor.preprocess_text(doc)))
        
        return {term: math.log(total_documents / doc_count) if doc_count > 0 else 0
                for term, doc_count in term_doc_count.items()}
    
    def calculate_tfidf_vector(self, document: str) -> Dict[str, float]:
        tokens = self.text_processor.preprocess_text(document)
        tf_scores = self.calculate_tf(tokens)
        return {term: tf_scores.get(term, 0) * self.idf_scores.get(term, 0) 
                for term in self.vocabulary}
    
    def cosine_similarity(self, vector1: Dict[str, float], vector2: Dict[str, float]) -> float:
        dot_product = sum(vector1.get(term, 0) * vector2.get(term, 0) for term in self.vocabulary)
        magnitude1 = math.sqrt(sum(score ** 2 for score in vector1.values()))
        magnitude2 = math.sqrt(sum(score ** 2 for score in vector2.values()))
        
        return dot_product / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0
    
    def fit(self, documents: List[str]):
        self.idf_scores = self.calculate_idf(documents)
    
    def get_recommendations(self, user_profile: str, event_documents: List[str], 
                          event_ids: List[int], limit: int = 10) -> List[Tuple[int, float]]:
        user_vector = self.calculate_tfidf_vector(user_profile)
        similarities = [(event_ids[i], self.cosine_similarity(user_vector, 
                        self.calculate_tfidf_vector(event_doc)))
                       for i, event_doc in enumerate(event_documents)]
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:limit]
