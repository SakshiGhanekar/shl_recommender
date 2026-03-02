import json
import numpy as np
import re
from rank_bm25 import BM25Okapi

class SHLRecommender:
    def __init__(self, data_path='assessments_full.json'):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
            
        self.data = [d for d in self.data if not d.get('error')]
        print(f"Loaded {len(self.data)} assessments.")
        
        def preprocess(text):
            text = text.lower()
            tokens = re.findall(r'\b\w+\b', text)
            return [t for t in tokens if len(t) > 1 or t in ['c', 'r', 'go', 'js']]

        self.corpus_texts = []
        for d in self.data:
            name = d.get('name', '')
            desc = d.get('description', '')
            combined = (name + " ") * 5 + desc
            self.corpus_texts.append(combined)
            
        self.tokenized_corpus = [preprocess(doc) for doc in self.corpus_texts]
        
        def get_bigrams(tokens):
            return [" ".join(tokens[i:i+2]) for i in range(len(tokens)-1)]
            
        self.token_docs = []
        for tokens in self.tokenized_corpus:
            self.token_docs.append(tokens + get_bigrams(tokens))
            
        self.bm25 = BM25Okapi(self.token_docs)
        
    def recommend(self, query, top_n=5):
        query = str(query)
        def preprocess(text):
            text = text.lower()
            tokens = re.findall(r'\b\w+\b', text)
            return [t for t in tokens if len(t) > 1 or t in ['c', 'r', 'go', 'js']]
            
        tokenized_query = preprocess(query)
        def get_bigrams(tokens):
            return [" ".join(tokens[i:i+2]) for i in range(len(tokens)-1)]
        
        q_tokens = tokenized_query + get_bigrams(tokenized_query)
        scores = self.bm25.get_scores(q_tokens)
        
        # Literal name boost: significant boost if query terms exist in assessment name
        for i, item in enumerate(self.data):
            name_lower = item['name'].lower()
            # More careful name match: avoid short common tokens
            relevant_q_tokens = [t for t in tokenized_query if len(t) > 3 or t in ['java', 'sql', 'cpp', 'html', 'seo']]
            for token in relevant_q_tokens:
                if token in name_lower:
                    scores[i] += 10.0 
        
        # Normalizing for result display
        if len(scores) > 0 and np.max(scores) > 0:
            norm_scores = scores / np.max(scores)
        else:
            norm_scores = scores
            
        top_indices = np.argsort(scores)[::-1][:top_n]
        
        recommendations = []
        for idx in top_indices:
            item = self.data[idx]
            recommendations.append({
                "Assessment name": item['name'],
                "URL": item['url'],
                "score": float(norm_scores[idx])
            })
            
        return recommendations
