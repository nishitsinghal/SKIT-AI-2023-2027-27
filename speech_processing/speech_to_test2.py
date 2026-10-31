
import re
import string
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")

def preprocess_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Tokenization
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    return " ".join(words)


# Read transcript
with open("transcript.txt", "r", encoding="utf-8") as file:
    text = file.read()

cleaned_text = preprocess_text(text)

# Save cleaned transcript
with open("cleaned_transcript.txt", "w", encoding="utf-8") as file:
    file.write(cleaned_text)

print("Original Text:", text)
print("\nCleaned Text:", cleaned_text)
print("\nPreprocessing completed!")
