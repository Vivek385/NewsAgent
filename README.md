AI News Aggregator
A simple yet powerful news aggregator web application built with Python and Streamlit. This app helps you stay up-to-date with the latest in Artificial Intelligence by consolidating news from your favorite RSS feeds into a single, clean interface.

🚀 Features
1. Default News Sources: Comes pre-loaded with a list of top-tier AI news sources.
2. Custom Feeds: Easily add your own favorite RSS feeds to create a personalized news dashboard.
3. Persistent Storage: Your custom feeds are saved locally in a user_feeds.json file, so they are remembered every time you launch the app.
4. Simple Interface: A clean and intuitive user interface built with Streamlit.

Easy to Use: No complex setup required. Get up and running in minutes.

🛠️ Installation & Setup
To run this application on your local machine, please follow these steps.

Prerequisites:

1. Python 3.7+
2. pip (Python package installer)

Steps:

1. Clone the repository:

```
git clone https://github.com/Vivek385/NewsAgent.git
cd NewsAgent
```

2. Install the required libraries:
```
pip install streamlit feedparser
```

3. Run the application:
```
streamlit run News_Agent.py
```
Your web browser will automatically open a new tab with the running application.

⚙️ How to Use the App

1. View News: By default, the app loads and displays the latest articles from the pre-configured feeds.
2. Filter Sources: Use the checkboxes in the sidebar to show or hide news from specific sources.

Add a Custom Feed:

1. Go to the "Add Your Own Feed" section in the sidebar.
2. Enter a unique name for the feed and its full RSS URL.
3. Click the "Add Feed" button. The feed will be saved and will appear in your "Custom Feeds" list.

Remove a Custom Feed:

3. Click the "🗑️" icon next to the custom feed you wish to remove.
4. The feed will be deleted from your list and the user_feeds.json file.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to contribute to this project by submitting a pull request or opening an issue.
