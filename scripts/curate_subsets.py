import json
import random
import os
from tqdm import tqdm
from util_filters import contain_numbers, contain_non_english, contain_unusual_proper_nouns

config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

script_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(script_dir, config["OUTPUT_DIR"])
DATA_PATH = os.path.join(script_dir, config["DATA_PATH"])

def filter_and_pick(data, filter_func, n=1000):
    """
    Filter and pick a subset of records from the data based on helper functions.
    """
    random.shuffle(data)
    picked = []
    for record in tqdm(data, desc="Processing records", unit="record"):
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
