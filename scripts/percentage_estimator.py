import json
from curate_subsets import contain_numbers, contain_non_english, contain_unusual_proper_nouns

DATA_PATH = "../data/JEOPARDY_QUESTIONS1.json"

def count_items(data, filter_func):
    count = 0
    for record in data:
        if filter_func(record['question']) or filter_func(record['answer']):
            count += 1
    return count

def main():
    with open(DATA_PATH, "r") as file:
        data = json.load(file)

    total_items = len(data)

    count_numbers = count_items(data, contain_numbers)
    count_non_english = count_items(data, contain_non_english)
    count_unusual_proper_nouns = count_items(data, contain_unusual_proper_nouns)
   
    percentage_numbers = round((count_numbers / total_items) * 100, 2)
    percentage_non_english = round((count_non_english / total_items) * 100, 2)
    percentage_unusual_proper_nouns = round((count_unusual_proper_nouns / total_items) * 100, 2)
  

    results = {
        "total_items": total_items,
        "items_with_numbers": {
            "count": count_numbers,
            "percentage": f"{percentage_numbers:.2f}%"
        },
        "items_with_non_english_content": {
            "count": count_non_english,
            "percentage": f"{percentage_non_english:.2f}%"
        },
        "items_with_unusual_proper_nouns": {
            "count": count_unusual_proper_nouns,
            "percentage": f"{percentage_unusual_proper_nouns:.2f}%"
        }
    }
    
    with open(COUNT_RESULT, "w") as outfile:
        json.dump(results, outfile, indent=4)

if __name__ == "__main__":
    main()
