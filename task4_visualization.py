import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def create_visualisations():
    date_str = datetime.now().strftime("%Y%m%d")
    csv_path = f"data/trends_{date_str}.csv"
    
    if not os.path.exists(csv_path):
        print("CSV file missing!")
        return
        
    df = pd.read_csv(csv_path)

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 6))
    category_order = df['category'].value_counts().index
    
    sns.countplot(data=df, x='category', order=category_order, palette="viridis")
    
    plt.title(f"HackerNews Story Distribution ({date_str})", fontsize=16)
    plt.xlabel("Category", fontsize=12)
    plt.ylabel("Number of Stories", fontsize=12)
    
    plt.savefig("data/category_distribution.png")
    print("Saved: data/category_distribution.png")
    plt.show()

    plt.figure(figsize=(10, 6))
    
    sns.barplot(data=df, x='category', y='score', palette="magma", ci=None)
    
    plt.title("Average HackerNews Score by Category", fontsize=16)
    plt.xlabel("Category", fontsize=12)
    plt.ylabel("Average Score", fontsize=12)

    plt.savefig("data/average_scores_plot.png")
    print("Saved: data/average_scores_plot.png")
    plt.show()

if __name__ == "__main__":
    create_visualisations()