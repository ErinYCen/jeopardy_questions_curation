import json
import random
from tqdm import tqdm
from util_filters import contain_numbers, contain_non_english, contain_unusual_proper_nouns

with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
COUNT_RESULT = config["COUNT_RESULT"]
SAMPLE_SIZE = config["SAMPLE_SIZE"]
DATA_PATH = config["DATA_PATH"]
"""
SAMPLE_SIZE is initially set to 3000 to avoid excessive runtime
"""

def count_items(data, filter_func):
    """
    Count the number of records passing the filter function.
    """
    count = 0
    for record in tqdm(data, desc=f"Processing with {filter_func.__name__}"):
        if filter_func(record['question']) or filter_func(record['answer']):
            count += 1
    return count

def main():
    """
    Calculate estimated number of items fell into each filter function.
    Output the result to a JSON file.
    """
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    total_items = len(data)
    
    # Select a sample dataset randomly
    sample_data = random.sample(data, min(SAMPLE_SIZE, total_items))
    sample_total_items = len(sample_data)

    count_numbers = count_items(sample_data, contain_numbers)
    count_non_english = count_items(sample_data, contain_non_english)
    count_unusual_proper_nouns = count_items(sample_data, contain_unusual_proper_nouns)

    # Calculate percentage of items passed each filter in the sample data
    # Percentages are rounded to two decimal places
    percentage_numbers = round((count_numbers / sample_total_items) * 100, 2)
    percentage_non_english = round((count_non_english / sample_total_items) * 100, 2)
    percentage_unusual_proper_nouns = round((count_unusual_proper_nouns / sample_total_items) * 100, 2)

    # Estimate total number of items passing each filter for the original dataset
    # Based on the sample data
    estimated_count_numbers = round((count_numbers / sample_total_items) * total_items)
    estimated_count_non_english = round((count_non_english / sample_total_items) * total_items)
    estimated_count_unusual_proper_nouns = round((count_unusual_proper_nouns / sample_total_items) * total_items)
   
    results = {
        "sample_size": SAMPLE_SIZE,
        "total_items": total_items,
        "estimates": {
            "items_with_numbers": {
                "sample_count": count_numbers,
                "estimated_total": estimated_count_numbers,
                "percentage": f"{percentage_numbers:.2f}%"
            },
            "items_with_non_english_content": {
                "sample_count": count_non_english,
                "estimated_total": estimated_count_non_english,
                "percentage": f"{percentage_non_english:.2f}%"
            },
            "items_with_unusual_proper_nouns": {
                "sample_count": count_unusual_proper_nouns,
                "estimated_total": estimated_count_unusual_proper_nouns,
                "percentage": f"{percentage_unusual_proper_nouns:.2f}%"
            }
        }
    }

    with open(COUNT_RESULT, "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=4)

    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
