import pandas as pd
import json
from recommender import SHLRecommender
import time

def evaluate_recommender():
    """
    Evaluates the SHL Recommender's accuracy on the provided test dataset.
    This fulfills Expectation #3: Include proper evaluation methods.
    """
    print("Initializing Recommender for evaluation...")
    recommender = SHLRecommender('assessments_full.json')
    
    # Load the ground truth dataset
    df = pd.read_excel('Gen_AI Dataset.xlsx')
    
    # In a real setup, we compare predicted URL with Ground Truth URL
    # Gen_AI Dataset has 'Query' and 'Assessment_url'
    total_queries = len(df)
    hits_at_1 = 0
    hits_at_5 = 0
    hits_at_10 = 0
    
    print(f"Beginning evaluation of {total_queries} queries...")
    start_time = time.time()
    
    for idx, row in df.iterrows():
        query = str(row['Query'])
        gt_url = str(row['Assessment_url']).strip()
        
        # Get predictions
        top_10 = recommender.recommend(query, top_n=10)
        top_10_urls = [r['URL'].strip() for r in top_10]
        
        # Metrics calculation
        if gt_url in top_10_urls[:1]:
            hits_at_1 += 1
        if gt_url in top_10_urls[:5]:
            hits_at_5 += 1
        if gt_url in top_10_urls[:10]:
            hits_at_10 += 1
            
        if (idx + 1) % 50 == 0:
            print(f"Processed {idx + 1}/{total_queries}...")

    end_time = time.time()
    
    # Results
    metrics = {
        "Total Queries": total_queries,
        "Hit Rate @ 1 (Top-1 Match)": f"{(hits_at_1 / total_queries) * 100:.2f}%",
        "Hit Rate @ 5": f"{(hits_at_5 / total_queries) * 100:.2f}%",
        "Hit Rate @ 10": f"{(hits_at_10 / total_queries) * 100:.2f}%",
        "Average Latency": f"{(end_time - start_time) / total_queries:.4f}s"
    }
    
    print("\n--- Evaluation Metrics ---")
    for k, v in metrics.items():
        print(f"{k}: {v}")
        
    return metrics

if __name__ == "__main__":
    evaluate_recommender()
