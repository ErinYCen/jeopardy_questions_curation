# Jeopardy Question Dataset Curation

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
