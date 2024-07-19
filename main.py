import streamlit as st
from googleapiclient.discovery import build
import isodate
from datetime import timedelta
import re

# YouTube API credentials
API_KEY = 'AIzaSyDq7-fCpGCmhx8pbw21jeCpk8nzyej68SA'

# Function to fetch YouTube playlist/video stats
def get_youtube_stats(url):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    stats = {}
    
    playlist_id = None
    video_id = None

    # Extract playlist ID or video ID from URL
    if "playlist" in url:
        playlist_id_match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
        if playlist_id_match:
            playlist_id = playlist_id_match.group(1)
    else:
        video_id_match = re.search(r'v=([a-zA-Z0-9_-]+)', url)
        if video_id_match:
            video_id = video_id_match.group(1)
    
    if playlist_id:
        try:
            playlist_response = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50
            ).execute()
            
            video_ids = [item['contentDetails']['videoId'] for item in playlist_response['items']]
            
            video_response = youtube.videos().list(
                part='contentDetails,statistics',
                id=','.join(video_ids)
            ).execute()
            
            total_length = timedelta()
            total_views = 0
            total_comments = 0
            total_likes = 0
            total_dislikes = 0
            
            for video in video_response['items']:
                duration = isodate.parse_duration(video['contentDetails']['duration'])
                total_length += duration
                total_views += int(video['statistics']['viewCount'])
                total_comments += int(video['statistics'].get('commentCount', 0))
                total_likes += int(video['statistics'].get('likeCount', 0))
                total_dislikes += int(video['statistics'].get('dislikeCount', 0))
            
            stats = {
                'Total Length': str(total_length),
                'Total Views': total_views,
                'Total Comments': total_comments,
                'Total Likes': total_likes,
                'Total Dislikes': total_dislikes
            }
        except Exception as e:
            st.error(f"Error fetching playlist statistics: {e}")
    elif video_id:
        try:
            video_response = youtube.videos().list(
                part='contentDetails,statistics',
                id=video_id
            ).execute()
            
            video = video_response['items'][0]
            duration = isodate.parse_duration(video['contentDetails']['duration'])
            
            stats = {
                'Length': str(duration),
                'Views': int(video['statistics']['viewCount']),
                'Comments': int(video['statistics'].get('commentCount', 0)),
                'Likes': int(video['statistics'].get('likeCount', 0)),
                'Dislikes': int(video['statistics'].get('dislikeCount', 0))
            }
        except Exception as e:
            st.error(f"Error fetching video statistics: {e}")
    else:
        st.error("Invalid YouTube URL. Please enter a valid playlist or video URL.")
    
    return stats

# Streamlit app configuration
st.set_page_config(page_title="YouTube Stats Analyzer", page_icon=":chart_with_upwards_trend:", layout="centered")

# Header
st.markdown("<h1 style='text-align: center; color: #FF0000;'>YouTube Stats Analyzer</h1>", unsafe_allow_html=True)

# SEO meta tags
st.markdown("""
    <meta name="description" content="Analyze YouTube playlist and video statistics including total length, views, and comments. Perfect for YouTube content creators and marketers.">
    <meta name="keywords" content="YouTube stats, YouTube analytics, YouTube playlist stats, YouTube video stats">
    <meta name="author" content="Your Name">
    <meta property="og:title" content="YouTube Stats Analyzer">
    <meta property="og:description" content="Analyze YouTube playlist and video statistics including total length, views, and comments.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="http://yourwebsite.com">
    <meta property="og:image" content="http://yourwebsite.com/og-image.jpg">
""", unsafe_allow_html=True)

# YouTube URL input and fetch button
url = st.text_input("Enter YouTube Playlist/Video URL:")

# Display stats
if st.button("Fetch Stats") and url:
    with st.spinner('Fetching statistics...'):
        stats = get_youtube_stats(url)
    
    if stats:
        st.markdown("<h2 style='color: #FF0000;'>Statistics</h2>", unsafe_allow_html=True)
        st.table(list(stats.items()))

# Ad integration
st.markdown("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
    <!-- Your AdSense Ad Unit -->
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
         data-ad-slot="YYYYYYYYYY"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
    """, unsafe_allow_html=True)

# SEO-friendly footer
st.markdown("""
    <footer style="text-align: center; padding: 10px;">
        <p>© 2024 YouTube Stats Analyzer. All rights reserved.</p>
        <p><a href="http://yourwebsite.com/privacy-policy" style="color: #FF0000;">Privacy Policy</a> | <a href="http://yourwebsite.com/terms-of-service" style="color: #FF0000;">Terms of Service</a></p>
    </footer>
    """, unsafe_allow_html=True)
