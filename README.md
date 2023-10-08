# View news from sites
Must have python. Tested on `python 3.11.3`.

## How to run
```bash
pip install -r requirements.txt
streamlit run src/main.py
```

## Add sites
Try changing `NEWS_URLS`. The second argument for each tuple is a filter for specific urls. Also, note that the website has `www` in it since I require uniform format and don't want to put effort into it.