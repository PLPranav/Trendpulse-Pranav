import json
import csv
import os
from datetime import datetime

def clean_and_convert():
    date_str = datetime.now().strftime("%Y%m%d")
    json_path = f"data/trends_{date_str}.json"
    
    print(f"Looking for input file: {json_path}...")

    if not os.path.exists(json_path):
        print(f"ERROR: {json_path} not found! Did Task 1 finish successfully?")
        return 

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("ERROR: JSON file is empty. Nothing to convert.")
        return

    csv_path = json_path.replace(".json", ".csv")
    
    headers = ["post_id", "title", "category", "score", "num_comments", "author", "collected_at"]
    
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for entry in data:
               
                cleaned_row = {
                    "post_id": entry.get("post_id"),
                    "title": entry.get("title"),
                    "category": entry.get("category"),
                    "score": entry.get("score") if entry.get("score") is not None else 0,
                    "num_comments": entry.get("num_comments") if entry.get("num_comments") is not None else 0,
                    "author": entry.get("author"),
                    "collected_at": entry.get("collected_at")
                }
                writer.writerow(cleaned_row)

        print(f"SUCCESS: Task 2 complete. Cleaned data saved to {csv_path}")
    
    except Exception as e:
        print(f"An error occurred during CSV writing: {e}")


if __name__ == "__main__":
    clean_and_convert()
