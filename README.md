# Youtube Data Collection using Google Cloud and YouTube API

### Table of Contents

1. Introduction
2. Features
3. Installation
4. Usage
5. Dataset Structure

# Introduction

This project uses Google Cloud services to interact with the YouTube API, allowing users to collect video statistics, and comments. The collected data is saved in a structured format within a dataset folder.

The request flow consists of retrieving channel IDs, video IDs, comments, and video statistics in a sequential manner. Users need to set all request parameters to True for the first-time setup.

Channel Handles are all that is needed. Channel handles are found on the YouTuber's channel with a '@' symbol. You can add more channel handles in the config file. 



# Features

- **YouTube Data Collection:** Collect channel IDs, video IDs, comments, and video statistics.
- **Automated Requests:** Request data sequentially in the following order:
    1. Channel ID's
    2. Video ID's
    3. Comments
    4. Video statistics
- **Google Cloud Integration:** Uses Google Cloud credentials to make requests through the YouTube Data API.
- **Dataset Storage:** All retrieved data is saved in a structured format under the dataset folder for access.

# Installation

To get started, clone the repository and install the required libraries.
```
git clone https://github.com/XXRG456/youtube_api.git
cd youtube_api
pip install -r requirements.txt
```

#### Setting up Google Cloud API

1. Create project in Google Cloud.
2. Enable the YouTube Data API v3.
3. Create API key.
4. Assign ```DEVELOPER_KEY = 'YOUR_API_KEY'``` in a .env file in current directory.

# Usage

1. In the config file set **retrieve_dataset** Parameter to **True**.
2. Run ```python main.py``` as is.
3. Once Dataset has been retrieved, set **retrieve_dataset** to **False** in the config file.
4. Now uncomment in main to load Comments and statistics.

