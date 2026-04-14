import pandas as pd
import numpy as np
import os
from datetime import datetime

def perform_analysis():
    date_str = datetime.now().strftime("%Y%m%d")
    csv_path = f"data/trends_{date_str}.csv"
    
    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_path} not found. Please run Task 2 first!")
        return 

    df = pd.read_csv(csv_path)

    print("\n" + "="*40)
    print("      TRENDPULSE ANALYSIS REPORT")
    print("="*40)

    counts = df['category'].value_counts()
    print("\n[1] Stories Collected per Category:")
    print(counts)

   
    print("\n[2] Average Scores per Category:")
    avg_scores = df.groupby('category')['score'].agg(np.mean).round(2)
    print(avg_scores)

    
    max_comm_idx = np.argmax(df['num_comments'].values)
    viral_story = df.iloc[max_comm_idx]

    print("\n[3] Most Discussed Story (Highest Comments):")
    print(f"Title: {viral_story['title']}")
    print(f"Comments: {viral_story['num_comments']}")
    print(f"Category: {viral_story['category']}")
    print("="*40 + "\n")

if __name__ == "__main__":
    perform_analysis()
