🌟 Features
Smart Batch Downloads
Fetch up to 100 vector images per search query

Auto-Organization
Saves to ~/Downloads/Vectors/[search_term]/ with sequential numbering

Progress Tracking
Real-time download progress bar

One-Click Access
"Open Folder" button immediately shows downloaded assets

Async Architecture
Non-blocking downloads using aiohttp and asyncio

🚀 Quick Start
Prerequisites
Python 3.7+

Pixabay API key (free tier available)

bash
```# Install dependencies
pip install aiohttp

# Run the application
python pixabay_harvester.py
```

🛠️ Configuration
Edit these constants in the script:
python
PIXABAY_API_KEY = "your-api-key-here"  # Required
RESULTS_PER_PAGE = 100                 # Max allowed by API
DOWNLOAD_FOLDER = "~/Downloads/Vectors" # Customizable path

📂 File Structure
text
pixabay-vector-harvester/
├── src/
│   └── pixabay_harvester.py  # Main application
├── outputs/                  # Default download location
│   └── Pixabay/
│       ├── cats/             # Example search term folder
│       └── dogs/
├── requirements.txt          # aiohttp only
└── README.md

🔧 How It Works
Search Phase:

python:
```
async def search_pixabay_images(query):
    url = f"https://pixabay.com/api/?key={API_KEY}&q={query}&image_type=vector"
    # ... API request handling ...
```
Download Phase:
Creates numbered files (query_01.png, query_02.png)
Handles duplicate filenames automatically
Updates progress bar during transfers

⚠️ Limitations
Currently only downloads PNG format
No pause/resume functionality
Basic error handling (will be improved in v2)

📜 License
MIT License - See LICENSE
