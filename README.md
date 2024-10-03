# Data Tracker: Drug Detection Tools

## Description
The **Data Tracker Drug Detection Tools** is a web-based application designed to detect drug mentions in chat messages and highlight them. It also provides a search tool for drug names and related details such as conditions treated and ratings from a dataset.

This tool is designed to assist in analyzing conversations and identifying mentions of drugs to help in various monitoring and detection scenarios.

## Features
- **Chat Drug Detection**: Enter chat text, and the system highlights any detected drug names.
- **Drug Search Tool**: Search for drug names from a preloaded dataset.
- **Rating Filter**: Only display drugs with a rating of 10.
- **Pagination**: Display drug search results with 10 entries per page.

## Prerequisites
- **Python 3.x**
- Flask (web framework)
- Pandas (data processing)

├── app.py                # Main application script
├── datasets/
│   └── drugsComTest_raw.csv # Drug dataset
├── templates/
│   └── index.html        # Homepage template
│   └── chat.html         # Chat detection template
├── static/
│   └── styles/
│       └── style.css     # CSS styles
├── requirements.txt      # Required Python packages
├── README.md             # Project documentation



### Instructions for Usage
1. **Replace the paths for the images in the Example section** with actual file paths for screenshots.
2. **Modify the repository link** (https://github.com/your-username/your-repository-name) with your actual GitHub repository URL.

