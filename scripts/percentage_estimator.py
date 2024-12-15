import json
from curate_subsets import contain_numbers, contain_non_english, contain_unusual_proper_nouns

DATA_PATH = "../data/JEOPARDY_QUESTIONS1.json"

def count_items(data, filter_func):
    count = 0
    for record in data:
        if filter_func(record['question']) or filter_func(record['answer']):
            count += 1
    return count

