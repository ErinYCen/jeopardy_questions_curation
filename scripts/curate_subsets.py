import json
import random
import re
import spacy
import requests

from py3langid.langid import LanguageIdentifier, MODEL_FILE

DATA_PATH = "../data/JEOPARDY_QUESTIONS1.json"
OUTPUT_DIR = "../data/"

nlp = spacy.load("en_core_web_md")

def contain_numbers(phrase):
    url_pattern = r'https?://[^\s]+'
    phrase_without_urls = re.sub(url_pattern, '', phrase)
    return bool(re.search(r'\d', phrase_without_urls))

def contain_non_english(phrase):
    identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
    tokens = phrase.split()

    non_english = [
        word for word in tokens
        if identifier.classify(word)[0] != 'en'
    ]

    print("Tokens:", tokens)
    print("Non-English Words:", non_english)

    return len(non_english) > 0

def query_wikidata_rarity(noun_tobecheck):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "language": "en",
        "format": "json",
        "search": noun_tobecheck,
    }
    response = requests.get(url, params=params)
    thisdata = response.json()

    if not thisdata.get("search"):
        return True

    for result in thisdata["search"]:
        description =  result.get("description", "").lower()
        if any(keyword in description for keyword in ["person", "city", "state", "country", "organization"]):
            return False
        if result.get("sitelinks", 0) > 50:
            return False
    return True

def contain_unusual_proper_nouns(phrase):
    doc = nlp(phrase)

    for sent in doc.sents:
        for ent in sent.ents:
            if ent.label_ in {"PERSON", "GPE", "ORG", "LOC", "FAC", "EVENT", "WORK_OF_ART", "LAW"} and query_wikidata_rarity(ent.text):
                return True
    return False

def filter_and_pick(data, filter_func, n=1000):
    random.shuffle(data)
    picked = []
    for record in data:
        if filter_func(record['question']) or filter_func(record['answer']):
            picked.append(record)
        if len(picked) >= n:
            break
    return picked

def main():

    with open(DATA_PATH, "r") as file:
        data = json.load(file)

    subset_numbers = filter_and_pick(data, contain_numbers, n=1000)
    subset_non_english = filter_and_pick(data, contain_non_english, n=1000)
    subset_unusual_proper_nouns = filter_and_pick(data, contain_unusual_proper_nouns, n=1000)

    with open(f"{OUTPUT_DIR}subset_numbers.jsonl", "w") as file:
        for obj in subset_numbers:
            file.write(json.dumps(obj) + '\n')
    with open(f"{OUTPUT_DIR}subset_non_english.jsonl", "w") as file:
        for obj in subset_non_english:
            file.write(json.dumps(obj) + '\n')
    with open(f"{OUTPUT_DIR}subset_unusual_proper_nouns.jsonl", "w") as file:
        for obj in subset_unusual_proper_nouns:
            file.write(json.dumps(obj) + '\n')

    print("Subsets generated")

if __name__ == "__main__":
    main()
