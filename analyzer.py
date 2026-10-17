
from collections import Counter

import fitz
import nltk
import spacy

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    ENGLISH_STOP_WORDS,
)

# Download the sentence tokenizer resource if needed.
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

# Load spaCy's pretrained English NLP model.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None


def extract_pdf(pdf_bytes):
    """Extract text and page count from a PDF."""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
        pages = [
            page.get_text("text", sort=True)
            for page in pdf
        ]
        page_count = len(pdf)

    return "\n\n".join(pages).strip(), page_count


def clean_text(text):
    """Clean text using Python string operations."""
    text = text.replace("\x00", " ")
    text = text.replace("-\n", "")
    text = " ".join(text.split())
    return text.strip()


def split_sentences(text):
    """Split text into sentences using NLTK."""
    try:
        sentences = nltk.sent_tokenize(text)
    except LookupError:
        nltk.download("punkt_tab", quiet=True)
        sentences = nltk.sent_tokenize(text)

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 5
    ]


def extract_keywords(text, top_n=15):
    """Rank important terms using TF-IDF."""
    sentences = split_sentences(text)

    if not sentences:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=3000,
    )

    try:
        matrix = vectorizer.fit_transform(sentences)
    except ValueError:
        return []

    scores = matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()

    ranked = sorted(
        zip(terms, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        (term, round(float(score), 4))
        for term, score in ranked[:top_n]
    ]


def summarize_text(text, max_sentences=6):
    """Extract important original sentences using word frequencies."""
    sentences = split_sentences(text)

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    if nlp is not None:
        doc = nlp(text[:1_000_000])
        words = [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha
            and not token.is_stop
            and len(token.text) > 2
        ]
    else:
        words = [
            word.lower()
            for word in text.split()
            if word.isalpha()
            and len(word) > 2
            and word.lower() not in ENGLISH_STOP_WORDS
        ]

    frequencies = Counter(words)

    if not frequencies:
        return " ".join(sentences[:max_sentences])

    max_frequency = max(frequencies.values())
    scored_sentences = []

    for index, sentence in enumerate(sentences):
        if nlp is not None:
            doc = nlp(sentence)
            tokens = [
                token.lemma_.lower()
                for token in doc
                if token.is_alpha
                and not token.is_stop
                and len(token.text) > 2
            ]
        else:
            tokens = [
                word.lower()
                for word in sentence.split()
                if word.isalpha()
                and len(word) > 2
                and word.lower() not in ENGLISH_STOP_WORDS
            ]

        score = (
            sum(frequencies[word] / max_frequency for word in tokens)
            / max(len(tokens), 1)
        )

        scored_sentences.append((score, index, sentence))

    best = sorted(
        sorted(scored_sentences, reverse=True)[:max_sentences],
        key=lambda item: item[1],
    )

    return " ".join(sentence for _, _, sentence in best)


def extract_entities(text):
    """Extract named entities with spaCy."""
    if nlp is None:
        return []

    doc = nlp(text[:100_000])

    entities = {
        (entity.text, entity.label_)
        for entity in doc.ents
    }

    return sorted(entities)


def analyze_paper(text):
    """Run NLP analysis on a research paper."""
    text = clean_text(text)

    if nlp is not None:
        doc = nlp(text[:1_000_000])
        words = [
            token.text
            for token in doc
            if token.is_alpha
        ]
    else:
        words = [
            word
            for word in text.split()
            if word.isalpha()
        ]

    sentences = split_sentences(text)

    frequent_terms = Counter(
        word.lower()
        for word in words
        if len(word) > 2
        and word.lower() not in ENGLISH_STOP_WORDS
    )

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "keywords": extract_keywords(text),
        "summary": summarize_text(text),
        "entities": extract_entities(text),
        "frequent_terms": frequent_terms.most_common(15),
        "clean_text": text,
    }
