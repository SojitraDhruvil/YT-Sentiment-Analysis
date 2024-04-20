import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')


df = pd.read_csv('../Data-Preprocessing/Merge_Data_Comment.csv')

# Define lists of keywords for each class
positive_keywords = ['great', 'amazing', 'excellent', 'good', 'appreciate', 'thank', 'best', 'awesome', 'wonderful', 'fantastic', 'love', 'loved','ok','okay','hi','hello','free','w','fantastic','amazing','respect']
negative_keywords = ['bad', 'terrible', 'worst', 'not able', 'could not', 'fail', 'poor', 'awful', 'hate', 'hated', 'dislike', 'disappointed','n','illegal','weird']
interrogative_keywords = ['what', 'why', 'how', 'when', 'where', 'can', 'could', 'how to', 'what is the', 'why is it', 'which']
imperative_keywords = ['let', 'try', 'follow', 'do', 'make', 'watch', 'start', 'stop', 'you should', 'you must', 'you need to']
corrective_keywords = ['correction', 'mistake', 'error', 'fix', 'remedy', 'improve', 'correction needed', 'needs improvement']

# Define stop words and stemmer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    # Check if the input is a string
    if not isinstance(text, str):
        return []

    # Tokenize the text into words
    tokens = word_tokenize(text.lower())

    # Remove stop words and stem the remaining words
    filtered_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]

    return filtered_tokens

def classify_comment(comment_text):
    # Check if the input is a string and not empty
    if not isinstance(comment_text, str) or not comment_text.strip():
        return 'Miscellaneous'

    tokens = preprocess_text(comment_text)

    if any(keyword in tokens for keyword in positive_keywords):
        return 'Positive'
    elif any(keyword in tokens for keyword in negative_keywords):
        return 'Negative'
    elif any(keyword in tokens for keyword in interrogative_keywords):
        return 'Interrogative'
    elif any(keyword in tokens for keyword in imperative_keywords):
        return 'Imperative'
    elif any(keyword in tokens for keyword in corrective_keywords):
        return 'Corrective'
    else:
        return 'Miscellaneous'

# Define a function to check for empty comments
def is_comment_empty(comment):
    if pd.isna(comment) or not comment.strip():
        return True
    else:
        return False

# Drop rows with empty comments
df = df[~df['Comment'].apply(is_comment_empty)]

# Add a new column 'Class' to the DataFrame
df['Class'] = df['Comment'].apply(classify_comment)

csv_file = 'New_Merge_Data_Comment.csv'
df.to_csv(csv_file, index=False)