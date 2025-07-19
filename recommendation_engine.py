
import math
from typing import List, Dict, Tuple
from collections import Counter
from utils.text_processing import TextProcessor

# Rest of your TFIDFRecommendationEngine class...



class TFIDFRecommendationEngine:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.vocabulary = set()
        self.idf_scores = {}
        self.document_vectors = []
        
    def calculate_tf(self, tokens: List[str]) -> Dict[str, float]:
        """Calculate Term Frequency for a document."""
        if not tokens:
            return {}
        
        token_count = Counter(tokens)
        doc_length = len(tokens)
        
        tf_scores = {}
        for token, count in token_count.items():
            tf_scores[token] = count / doc_length
            
        return tf_scores
    
    def calculate_idf(self, documents: List[str]) -> Dict[str, float]:
        """Calculate Inverse Document Frequency for vocabulary."""
        total_documents = len(documents)
        if total_documents == 0:
            return {}
        
        # Get vocabulary from all documents
        self.vocabulary = self.text_processor.get_vocabulary(documents)
        
        # Count documents containing each term
        term_doc_count = {}
        for term in self.vocabulary:
            term_doc_count[term] = 0
            
        for doc in documents:
            tokens = set(self.text_processor.preprocess_text(doc))
            for term in tokens:
                if term in term_doc_count:
                    term_doc_count[term] += 1
        
        # Calculate IDF scores
        idf_scores = {}
        for term, doc_count in term_doc_count.items():
            if doc_count > 0:
                idf_scores[term] = math.log(total_documents / doc_count)
            else:
                idf_scores[term] = 0
                
        return idf_scores
    
    def calculate_tfidf_vector(self, document: str) -> Dict[str, float]:
        """Calculate TF-IDF vector for a single document."""
        tokens = self.text_processor.preprocess_text(document)
        tf_scores = self.calculate_tf(tokens)
        
        tfidf_vector = {}
        for term in self.vocabulary:
            tf = tf_scores.get(term, 0)
            idf = self.idf_scores.get(term, 0)
            tfidf_vector[term] = tf * idf
            
        return tfidf_vector
    
    def cosine_similarity(self, vector1: Dict[str, float], vector2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two TF-IDF vectors."""
        # Calculate dot product
        dot_product = 0
        for term in self.vocabulary:
            dot_product += vector1.get(term, 0) * vector2.get(term, 0)
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(score ** 2 for score in vector1.values()))
        magnitude2 = math.sqrt(sum(score ** 2 for score in vector2.values()))
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def fit(self, documents: List[str]):
        """Fit the TF-IDF model on a corpus of documents."""
        self.idf_scores = self.calculate_idf(documents)
        
        # Pre-calculate TF-IDF vectors for all documents
        self.document_vectors = []
        for doc in documents:
            vector = self.calculate_tfidf_vector(doc)
            self.document_vectors.append(vector)
    
    def get_recommendations(self, user_profile: str, event_documents: List[str], 
                          event_ids: List[int], limit: int = 10) -> List[Tuple[int, float]]:
        """
        Get event recommendations based on user profile.
        Returns list of (event_id, similarity_score) tuples.
        """
        # Calculate user profile TF-IDF vector
        user_vector = self.calculate_tfidf_vector(user_profile)
        
        # Calculate similarities with all events
        similarities = []
        for i, event_doc in enumerate(event_documents):
            event_vector = self.calculate_tfidf_vector(event_doc)
            similarity = self.cosine_similarity(user_vector, event_vector)
            similarities.append((event_ids[i], similarity))
        
        # Sort by similarity score (descending) and return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:limit]
