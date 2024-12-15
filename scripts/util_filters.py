import json
import re
import spacy
import requests

from py3langid.langid import LanguageIdentifier, MODEL_FILE

nlp = spacy.load("en_core_web_md")

def contain_numbers(phrase):
    """
    Check if the text contains any numeric characters.
    Exclude numbers in url links.
    """
    url_pattern = r'https?://[^\s]+'
    phrase_without_urls = re.sub(url_pattern, '', phrase)
    return bool(re.search(r'\d', phrase_without_urls))

def contain_non_english(phrase):
    """
    Check if the text contains non-English words.
    Known issue: Struggle with abbrevations, verb morphological changes, and rare names.
    """
    identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
    tokens = phrase.split()

    non_english = [
        word for word in tokens
        if identifier.classify(word)[0] != 'en'
    ]

    return len(non_english) > 0

def query_wikidata_rarity(noun_tobecheck):
    """
    Check the rarity of a given noun using the Wikidata API.
    """
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
        description = result.get("description", "").lower()
        if any(keyword in description for keyword in ["person", "city", "state", "country", "organization"]):
            return False
        if result.get("sitelinks", 0) > 50:
            return False
    return True

def contain_unusual_proper_nouns(phrase):
    """
    Check if the text contains unusual proper nouns.
    """
    doc = nlp(phrase)

    for sent in doc.sents:
        for ent in sent.ents:
            if ent.label_ in {"PERSON", "GPE", "ORG", "LOC", "FAC", "EVENT", "WORK_OF_ART", "LAW"} and query_wikidata_rarity(ent.text):
                return True
    return False
