# main.py
import streamlit as st
import feedparser
from datetime import datetime
import time
import json
import os

# --- App Configuration ---
st.set_page_config(
    page_title="AI News Aggregator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Constants ---
FEEDS_FILE = "user_feeds.json"

# A dictionary of default RSS feeds to fetch news from.
DEFAULT_RSS_FEEDS = {
    "Ars Technica (AI)": "http://feeds.arstechnica.com/arstechnica/artificial-intelligence",
    "VentureBeat (AI)": "https://venturebeat.com/category/ai/feed/",
    "MIT News (AI)": "https://news.mit.edu/topic/artificial-intelligence2/rss",
    "ScienceDaily (AI)": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
    "TechCrunch (AI)": "https://techcrunch.com/category/artificial-intelligence/feed/",
}

# --- Functions for Persistence ---

def load_user_feeds():
    """Loads user-added feeds from the JSON file."""
    if not os.path.exists(FEEDS_FILE):
        return {}
    try:
        with open(FEEDS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Handle cases where the file is empty or corrupted
        return {}

def save_user_feeds(feeds):
    """Saves user-added feeds to the JSON file."""
    with open(FEEDS_FILE, "w") as f:
        json.dump(feeds, f, indent=4)

# --- Initialize Session State ---
# Load user feeds from the JSON file only once when the app starts.
if 'user_feeds' not in st.session_state:
    st.session_state.user_feeds = load_user_feeds()

# --- Core Functions ---

def fetch_feed(feed_url):
    """
    Parses an RSS feed and returns the parsed data.
    Includes basic error handling for feed parsing.
    """
    try:
        return feedparser.parse(feed_url)
    except Exception as e:
        st.error(f"Error fetching feed: {feed_url}")
        st.error(str(e))
        return None

def format_date(published_tuple):
    """
    Formats the publication date from the feed into a more readable string.
    """
    if published_tuple:
        try:
            dt = datetime.fromtimestamp(time.mktime(published_tuple))
            return dt.strftime('%a, %d %b %Y %H:%M:%S')
        except Exception:
            return "Date not available"
    return "Date not available"

# --- UI Layout ---

# Title of the application
st.title("📰 Top AI News for Today")
st.markdown("Your daily digest of the latest developments in Artificial Intelligence, consolidated in one place.")
st.markdown("---")

# --- Sidebar ---
st.sidebar.title("News Sources")

# --- Display and Select Feeds ---
selected_feeds = {}

st.sidebar.subheader("Default Feeds")
for name, url in DEFAULT_RSS_FEEDS.items():
    selected_feeds[name] = st.sidebar.checkbox(name, value=True, key=f"cb_{name}")

st.sidebar.subheader("Your Custom Feeds")
if not st.session_state.user_feeds:
    st.sidebar.info("You haven't added any custom feeds yet.")

# Create a copy to iterate over, allowing for deletion
user_feeds_copy = st.session_state.user_feeds.copy()
for name, url in user_feeds_copy.items():
    col1, col2 = st.sidebar.columns([0.85, 0.15])
    with col1:
        selected_feeds[name] = st.checkbox(name, value=True, key=f"cb_{name}")
    with col2:
        if st.button("🗑️", key=f"del_{name}", help=f"Remove {name}"):
            # Remove the feed and save the updated list
            del st.session_state.user_feeds[name]
            save_user_feeds(st.session_state.user_feeds)
            st.rerun()

# --- Add Custom Feed Section in Sidebar ---
st.sidebar.markdown("---")
st.sidebar.subheader("Add Your Own Feed")
with st.sidebar.form(key="add_feed_form", clear_on_submit=True):
    new_feed_name = st.text_input("Feed Name (e.g., My Favorite Blog)")
    new_feed_url = st.text_input("RSS Feed URL")
    submit_button = st.form_submit_button(label="Add Feed")

    if submit_button:
        if new_feed_name and new_feed_url:
            all_feed_names = list(DEFAULT_RSS_FEEDS.keys()) + list(st.session_state.user_feeds.keys())
            if new_feed_name not in all_feed_names:
                st.session_state.user_feeds[new_feed_name] = new_feed_url
                save_user_feeds(st.session_state.user_feeds)
                st.sidebar.success(f"'{new_feed_name}' added!")
                time.sleep(1) # Give user time to see the success message
                st.rerun()
            else:
                st.sidebar.warning("A feed with this name already exists.")
        else:
            st.sidebar.error("Please provide both a name and a URL.")

# --- Main Content Area ---
st.header("Latest Articles")

# Combine all feeds for fetching
all_feeds = {**DEFAULT_RSS_FEEDS, **st.session_state.user_feeds}
any_feed_selected = any(selected_feeds.get(name) for name in all_feeds)

if not any_feed_selected:
    st.warning("No news sources selected. Please select at least one source from the sidebar.")
else:
    # Loop through the combined list of feeds
    for name, url in all_feeds.items():
        if selected_feeds.get(name):
            with st.spinner(f"Fetching news from {name}..."):
                feed_data = fetch_feed(url)

            if feed_data and feed_data.entries:
                st.subheader(f"Feed: {name}")
                for entry in feed_data.entries[:10]: # Display top 10 articles
                    st.markdown(f"#### [{entry.title}]({entry.link})")
                    pub_date = format_date(entry.get("published_parsed"))
                    st.caption(f"Published: {pub_date}")
                    if "summary" in entry:
                        with st.expander("Read summary"):
                            st.markdown(entry.summary, unsafe_allow_html=True)
                    st.markdown("---")
            elif feed_data:
                st.warning(f"No articles found for {name}.")
            else:
                st.error(f"Could not retrieve articles for {name}.")

# --- Footer ---
st.markdown("---")
st.markdown("This app aggregates the latest news articles related to Artificial Intelligence from various sources, including both default and user-added RSS feeds. You can customize your news sources by adding your own RSS feed URLs.")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io)")
st.markdown("© 2023 AI News Aggregator. All rights reserved.")