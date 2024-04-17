from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer
from nltk import Counter
from deep_translator import GoogleTranslator
from collections import Counter
import re
import nltk
import itertools


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words_en = set(stopwords.words('english'))
stop_words_es = set(stopwords.words('spanish'))

lemmatizer = WordNetLemmatizer()

def translate_to_english(text:str):

    """ This function translates a text into English"""

    translated = GoogleTranslator(source='auto', target='en').translate(text)

    return translated


def get_wordnet_pos(tag):

    """Map POS tag to WordNet POS tag"""
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def preprocess_text(text : str):
    """
    This function receives a text and 
    eliminates characters, tokenizes and 
    lemmatizes.
    """

    # Traslate text into english

    text_en = translate_to_english(text)

    # Delete characters

    text_alpha_only = re.sub(r'[^a-zA-ZñÑáéíóúÁÉÍÓÚ]', ' ', text_en)

    # Tokenization
    tokens = word_tokenize(text_alpha_only)
    tagged_tokens = nltk.pos_tag(tokens)
    
    lemmatized_tokens = [lemmatizer.lemmatize(word.lower(), get_wordnet_pos(tag)) for word, tag in tagged_tokens if get_wordnet_pos(tag) == wordnet.NOUN ]

    word_counts = Counter(lemmatized_tokens)

    filtered_words = {word for word in word_counts.keys() if word not in stop_words_en and word not in stop_words_es and len(word)>2}

    return filtered_words

def filter_words(text,filtered_words):

    """ This fuction filters the words in
    a text using a list of words"""

    return [token for token in text if token in filtered_words]