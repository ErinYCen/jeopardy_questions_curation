# Jeopardy Question Dataset Curation
This project curates subsets of Jeopardy questions to validate Named Entity Recognition (NER) models. 
It creates subsets tailored for:
1. Phrases containing numbers.
2. Phrases containing non-English words.
3. Phrases containing unusual proper nouns.
## Dataset Curation Process
### Feature Selection
Among all the features in this dataset, only "Question" and "Answer" were selected to curate subsets.

The following features were excluded due to being numeric, the showing false positives for one of the subsets, and relatively irrelevant for this task:
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
- Detected using py3langid(explained below).
- Tokenized the "Question" and "Answer" features.
- Tokens are classified by language, and any token not identified as English (en) is marked as non-English. 
- Known issues: Struggles with abbreviations(eg: B&B), verb morphological changes(eg: espousing), and rare names(eg: Clinton).

3. Phrases containing unusual proper nouns
- Extracted using the spaCy NER model to identify entities labeled as PERSON, GPE, ORG, LOC, etc.
- These entities are queried against Wikidata to determine their rarity.
- An entity is marked "unusual" if it doesn't have common keywords(eg: New York, London) or has less than 50 sitelinks (an indicator of high prominence in Wikidata).
- Goal: Ensure most questions feature unusual proper nouns, though this method may have a high false-negative rate.
### Output
- The implementation consists of two separate Python files: one for generating subsets and another for estimating the number of items.
- Subsets are output in JSONL format, as it allows batch reading instead of loading the entire file at once.
- For estimation, the SAMPLE_SIZE is set to 3000 to avoid excessive runtime, as larger sample sizes can be significantly slower.
## Third Party Libraries
1. requests:
- An HTTP library for making web requests.
- Used in query_wikidata_rarity to interact with Wikidata's API for entity rarity evaluation.

2. Wikidata API
- A web-based interface that allows to interact with Wikidata, a free and open knowledge base maintained by the Wikimedia Foundation. 
- Provides structured data that can be accessed, queried, and updated via HTTP requests.

3. py3langid
- A lightweight library for language identification.
- Used in contain_non_english to classify individual words in the dataset as English (en) or another language.

4. SpaCy:
- An NLP library for text processing.
- Used in contain_unusual_proper_nouns for extract named entities.
- nlp.en_core_web_md: a pre-trained medium-sized English model for spacy.

5. tqdm
- A lightweight and versatile Python library for adding progress bars to loops, making it easy to monitor task progress.

## Installation
### Clone the Repository
```
git clone git@github.com:ErinYCen/jeopardy_questions_curation.git
cd jeopardy_questions_curation
```
### Install Dependencies
```
pip3 install -r requirements.txt
```
### Download SpaCy Model
```
python3 -m spacy download en_core_web_md
```
## Usage
### Generate Subsets
```
python3 scripts/curate_subsets.py
```
Output files are in data/ directory in JSONL format.
### Estimate Dataset Counts
```
python3 percentage_estimator.py 
```
## Acknowledgements
- Original dataset source: [Jeopardy Questions](https://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file/)

