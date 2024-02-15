import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from PyPDF2 import PdfReader
from spacy.matcher import Matcher

def get_parser():
    nlp = spacy.load('en_core_web_md')
    skill_path = 'data/skills.jsonl'

    ruler = nlp.add_pipe("entity_ruler")
    ruler.from_disk(skill_path)

    # patterns = [
    #     {"label": "PHONE NUMBER", "pattern": [{"ORTH": "("},  {"SHAPE": "ddd"}, {"ORTH": ")"}, {"SHAPE": "ddd"},
    #                                             {"ORTH": "-", "OP": "?"}, {"SHAPE": "dddd"}]}
    # ]

    # ruler.add_patterns(patterns)

    return nlp

#clean our data
def preprocessing(sentence, nlp):
    stopwords    = list(STOP_WORDS)
    doc          = nlp(sentence)
    clean_tokens = []
    
    for token in doc:
        if token.text not in stopwords and token.pos_ != 'PUNCT' and token.pos_ != 'SYM' and \
            token.pos_ != 'SPACE':
                clean_tokens.append(token.lemma_.lower().strip())
                
    return " ".join(clean_tokens)

def get_skills(text, nlp):
    
    return extract_(text, nlp, "SKILL")

def get_work_experience(text, nlp):

    return extract_(text, nlp, "ORG")

def get_email(text, nlp):
    # Define the pattern for email addresses
    email_pattern = [{"TEXT": {"REGEX": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"}}]

    # Initialize the matcher
    matcher = Matcher(nlp.vocab)
    matcher.add("EMAIL", [email_pattern])

    # Find matches in the processed text
    doc = nlp(text)
    matches = matcher(doc)

    # Extract email addresses from matches
    email_addresses = []
    for match_id, start, end in matches:
        span = doc[start:end]
        email_addresses.append(span.text)

    return email_addresses

def get_phone_number(text, nlp):
    # Define the pattern for email addresses
    phone_pattern = [
        {"TEXT": {"REGEX": r"\+?\d{1,3}"}},  # Country code, which is optional
        {"IS_SPACE": True, "OP": "?"},       # Optional space
        {"ORTH": "-"},                       # Hyphen
        {"IS_SPACE": True, "OP": "?"},       # Optional space
        {"TEXT": {"REGEX": r"\d{2,3}"}},     # Area code
        {"IS_SPACE": True, "OP": "?"},       # Optional space
        {"ORTH": "-"},                       # Hyphen
        {"IS_SPACE": True, "OP": "?"},       # Optional space
        {"TEXT": {"REGEX": r"\d{3,4}"}},     # First part of the number
        {"IS_SPACE": True, "OP": "?"},       # Optional space
        {"ORTH": "-"},                       # Hyphen
        {"IS_SPACE": True, "OP": "?"},       # Optional space
        {"TEXT": {"REGEX": r"\d{4}"}}        # Second part of the number
    ]

    # Initialize the matcher
    matcher = Matcher(nlp.vocab)
    matcher.add("PHONE NUMBER", [phone_pattern])

    # Find matches in the processed text
    doc = nlp(text)
    matches = matcher(doc)

    # Extract email addresses from matches
    phone_numbers = []
    for match_id, start, end in matches:
        span = doc[start:end]
        phone_numbers.append(span.text)

    return phone_numbers

def extract_(text, nlp, section):
    doc = nlp(text)
    
    result = []

    for ent in doc.ents:
        if ent.label_ == section:  # Assuming the company names are labeled as organizations
            result.append(ent.text)

    return result

def unique(x):
    return list(set(x))

def read_pdf(path):
    reader = PdfReader("data/chaklam_resume.pdf")
    page = reader.pages[0]
    text = page.extract_text()

    return text