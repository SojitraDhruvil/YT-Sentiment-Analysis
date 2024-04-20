
from googleapiclient.discovery import build
import pandas as pd
import getpass
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from autocorrect import Speller
import emoji
import string
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
nltk.download('punkt')


# YouTube Data API
# api_key = "AIzaSyCw2Jv32VeeGUx3cd_t1E85XlQ-KpZGCBM"
api_key = "AIzaSyARddhV0r2iP7sdnb9yWdjDxvceZw8ViL0"
# api_key = "AIzaSyDG1D34FAEtIVK_o9JcjWD_owY-v2LG8os"

youtube = build('youtube', 'v3', developerKey=api_key)


'''-------------------------------------------------------------'''


# Function to extract youtube ids (either video_id or playlist_id)
def extract_youtube_ids(input_string):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|playlist\?list=)|youtu.be/)([a-zA-Z0-9_-]+)'
    matches = re.findall(pattern, input_string)
    return matches

# Function to get user input for YouTube videos
def get_youtube_videos():
    input_string = input("Enter YouTube video URLs separated by commas: ")
    video_ids = extract_youtube_ids(input_string)
    return video_ids

# Function to get user input for YouTube playlists
def get_youtube_playlists():
    input_string = input("Enter YouTube playlist URLs separated by commas: ")
    playlist_ids = extract_youtube_ids(input_string)
    return playlist_ids


'''-------------------------------------------------------------'''


# Main function
print("Choose an option:")
print("1. Enter YouTube video URLs")
print("2. Enter YouTube playlist URLs")
choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    video_ids = get_youtube_videos()
    print("Extracted video IDs:", video_ids)
elif choice == '2':
    playlist_ids = get_youtube_playlists()
    print("Extracted playlist IDs:", playlist_ids)
    
    #extracting video_id from 
    def get_all_video_ids_from_playlists(youtube, playlist_ids):
        all_videos = []  # Initialize a single list to hold all video IDs

        for playlist_id in playlist_ids:
            next_page_token = None

            # Fetch videos from the current playlist
            while True:
                playlist_request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token)
                playlist_response = playlist_request.execute()

                all_videos += [item['contentDetails']['videoId'] for item in playlist_response['items']]

                next_page_token = playlist_response.get('nextPageToken')

                if next_page_token is None:
                    break

        return all_videos

    video_ids = get_all_video_ids_from_playlists(youtube, playlist_ids)
    print(len(video_ids))

else:
    print("Invalid choice. Please enter either 1 or 2.")


'''-------------------------------------------------------------'''


# Fetching replies from each and every videos
print("Fetching replies from youtube video_ids")
# Function to get replies for a specific comment
def get_replies(youtube, parent_id, video_id):
    replies = []
    next_page_token = None

    while True:
        reply_request = youtube.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText",
            maxResults=100,
            pageToken=next_page_token
        )
        reply_response = reply_request.execute()

        for item in reply_response['items']:
            comment = item['snippet']
            replies.append({
                'Timestamp': comment['publishedAt'],
                'Username': comment['authorDisplayName'],
                'VideoID': video_id,
                'Comment': comment['textDisplay'],
                'Date': comment['updatedAt'] if 'updatedAt' in comment else comment['publishedAt']
            })

        next_page_token = reply_response.get('nextPageToken')
        if not next_page_token:
            break

    return replies

# Function to get all top-level comments for a single video
def get_comments_for_video(youtube, video_id):
    all_comments = []
    next_page_token = None

    while True:
        comment_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=next_page_token,
            textFormat="plainText",
            maxResults=100
        )
        comment_response = comment_request.execute()

        for item in comment_response['items']:
            top_comment = item['snippet']['topLevelComment']['snippet']
            all_comments.append({
                'Timestamp': top_comment['publishedAt'],
                'Username': top_comment['authorDisplayName'],
                'VideoID': video_id,
                'Comment': top_comment['textDisplay'],
                'Date': top_comment['updatedAt'] if 'updatedAt' in top_comment else top_comment['publishedAt']
            })

        next_page_token = comment_response.get('nextPageToken')
        if not next_page_token:
            break

    return all_comments


'''-------------------------------------------------------------'''

# List to hold all comments from all videos
print("Storing comments in CSV file")
all_comments = []

for video_id in video_ids:
    video_comments = get_comments_for_video(youtube, video_id)
    all_comments.extend(video_comments)

comments_df = pd.DataFrame(all_comments)


'''-------------------------------------------------------------'''

# Storing comments in the csv format (I selected 4 playlist to fetch the comments from so I am storing in three csv file one by one and then at the end merging them.)

# csv_file = 'Data_Comment_1.csv'
# comments_df.to_csv(csv_file,index=False)

csv_file = 'Data_Comment_2.csv'
comments_df.to_csv(csv_file,index=False)

# csv_file = 'Data_Comment_3.csv'
# comments_df.to_csv(csv_file,index=False)
print("Process Done")