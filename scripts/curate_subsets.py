import json
import random
from util_filters import contain_numbers, contain_non_english, contain_unusual_proper_nouns

DATA_PATH = "../data/JEOPARDY_QUESTIONS1.json"

with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
OUTPUT_DIR = config["OUTPUT_DIR"]

def filter_and_pick(data, filter_func, n=1000):
    """
    Filter and pick a subset of records from the data based on helper functions.
    """
    random.shuffle(data)
    picked = []
    for record in data:
        if filter_func(record['question']) or filter_func(record['answer']):
            picked.append(record)
        if len(picked) >= n:
            break
    return picked

def main():
    """
    Process data and generate subsets based on filter functions.
    Output subsets to separate JSONL files.
    """

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    subset_numbers = filter_and_pick(data, contain_numbers, n=1000)
    subset_non_english = filter_and_pick(data, contain_non_english, n=1000)
    subset_unusual_proper_nouns = filter_and_pick(data, contain_unusual_proper_nouns, n=1000)

    with open(f"{OUTPUT_DIR}subset_numbers.jsonl", "w", encoding="utf-8") as file:
        for obj in subset_numbers:
            file.write(json.dumps(obj) + '\n')
    with open(f"{OUTPUT_DIR}subset_non_english.jsonl", "w", encoding="utf-8") as file:
        for obj in subset_non_english:
            file.write(json.dumps(obj) + '\n')
    with open(f"{OUTPUT_DIR}subset_unusual_proper_nouns.jsonl", "w", encoding="utf-8") as file:
        for obj in subset_unusual_proper_nouns:
            file.write(json.dumps(obj) + '\n')

    print("Subsets generated")

if __name__ == "__main__":
    main()
