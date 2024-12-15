# Jeopardy Question Dataset Curation
This project curates subsets of Jeopardy questions to validate Named Entity Recognition (NER) algorithms. 
It creates subsets tailored for:
- Phrases containing numbers.
- Phrases containing non-English words.
- Phrases containing unusual proper nouns.
## Dataset Curation Process
### Feature Selection
Among all the features in this dataset, I selected only "Question" and "Answer" to curate subsets.
The following features were excluded because they are numeric and reletively irrelevant for this task
- air_date: "YYYY-MM-DD"
- value: The value of the question
- show_number: The show ID where the question aired
The following features are already self-classified and were not included:
- category: The category of the question
- round: The round in which the question was asked, are already self-classified.
### Curation Process
1. Phrases containing numbers
- Identified using regular expressions to detect numeric characters (\d) within the "Question" and "Answer" features.
- URLs are removed beforehand to prevent false positives from picture links.

2. Phrases containing non-English words
- Detected using py3langid.
- Tokens in the "Question" and "Answer" features are classified by language, and any token not identified as English (en) is marked as non-English. 
- Known issues: Struggles with abbreviations, verb morphological changes, and rare names.

3. Phrases containing unusual proper nouns
- Extracted using the spaCy NER model to identify entities labeled as PERSON, GPE, ORG, LOC, etc.
- These entities are queried against Wikidata to determine their rarity.
- An entity is marked "unusual" if it lacks relevant descriptions or has limited associated links(low prominence).
- Goal:Ensure most questions feature unusual proper nouns, though this method may have a high false-negative rate.

## Third Party Libraries
1. requests:
- An HTTP library for making web requests.
- Used in query_wikidata_rarity to interact with Wikidata's API for entity rarity evaluation.

2. py3langid
- A lightweight library for language identification.
- Used in contain_non_english to classify individual words in the dataset as English (en) or another language.

3. spacy:
- An NLP library for text processing.
- Usd in contain_unusual_proper_nouns for extract named entities.
- nlp.en_core_web_md: a pre-trained small English model for spacy.

## Installation
### Clone the Repository
```
git clone git@github.com:ErinYCen/jeopardy_questions_curation.git
cd jeopardy_questions_curation
```
### Install Dependencies
```
pip install -r requirements.txt
```
If using Python 3.x:
```
pip3 install -r requirements.txt
```
### Download SpaCy Model
```
python -m spacy download en_core_web_md
```
If using Python 3.x:
```
python3 -m spacy download en_core_web_md
```
## Usage
### Generate Subsets
```
python scripts/curate_subsets.py
```
If using Python 3.x:
```
python3 scripts/curate_subsets.py
```
Output files are in data/ directory in JSONL format
### Estimate Dataset Counts
```
python percentage_estimator.py 
```
If using Python 3.x:
```
python3 percentage_estimator.py 
```
## Acknowledgements
- Original dataset source: [Jeopardy Questions](https://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file/)

