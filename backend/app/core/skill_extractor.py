import spacy
from spacy.matcher import PhraseMatcher
from app.core.skills_data import SKILLS_LIST

# Load the small English model once, at import time (expensive to reload per-request)
nlp = spacy.load("en_core_web_sm")

# Build the PhraseMatcher once, with all known skills registered
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")  # LOWER = case-insensitive matching
patterns = [nlp.make_doc(skill) for skill in SKILLS_LIST]
matcher.add("SKILLS", patterns)


def extract_skills(text: str) -> list[str]:
    """
    Scan the given text and return a list of unique skills found,
    matched against our curated SKILLS_LIST.
    """
    doc = nlp(text)
    matches = matcher(doc)

    found_skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        found_skills.add(span.text)

    return sorted(found_skills)