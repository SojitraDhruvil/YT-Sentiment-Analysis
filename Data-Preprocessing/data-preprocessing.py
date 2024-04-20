import pandas as pd
import re
import emoji
from autocorrect import Speller
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#Concatenate of two csv files
df1 = pd.read_csv('../Data-Gathering/Data_Comment_1.csv')
df2 = pd.read_csv('../Data-Gathering/Data_Comment_2.csv')
comments_df = pd.concat([df1,df2])
comments_df.to_csv('Merge_Data_Comment.csv', index=False)


# Removing certain rows from csv file like timestamp,username,date only keeping videoID and comments
df = pd.read_csv('Merge_Data_Comment.csv')
df = df.drop(['Date', 'Timestamp', 'Username'], axis=1)
df.to_csv('Merge_Data_Comment.csv', index=False)


# Data Preprocessing like lowering the value, removing emojis, removing stopwords, removing special characters like [,.;:!?|()%$#@^&{}]


df = pd.read_csv('Merge_Data_Comment.csv')

# Define a function to preprocess the comments
def preprocess_text(text):
    if isinstance(text, str):
        text = emoji.replace_emoji(text, replace='')
        text = re.sub(r'\b\d{5,}\b', '', text)
    else:
        # Handle non-string values (e.g., NaN, numeric)
        text = str(text)

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [w for w in word_tokens if not w in stop_words]
    text = ' '.join(filtered_text)
    text = re.sub(r'[\[,.;:!?|()%$#@^&{}\]]', '', text)
    text = text.lower()
    # spell = Speller(lang='en')
    # text = ' '.join([spell(word) for word in text.split()])

    return text

df['Comment'] = df['Comment'].apply(preprocess_text)
df.to_csv('Merge_Data_Comment.csv', index=False)

# Removing videoID from main comments data csv and storing it in other csv file.

df = pd.read_csv('Merge_Data_Comment.csv')
unique_video_ids = df['VideoID'].unique()
video_ids_df = pd.DataFrame({'VideoID': unique_video_ids})
video_ids_df.to_csv('unique_video_ids.csv', index=False)

df = df.drop(['VideoID'], axis=1)
