# Stock Analysis - Streamlit App

## Files
- `app.py`: Home page
- `pages/1_Market_Analysis.py`: EDA results and charts
- `pages/2_Stock_Explorer.py`: Interactive stock selector and date filter
- `stocks_cleaned.csv`: Your cleaned dataset (copy this file into this folder)
- `requirements.txt`: Python packages

## Setup (Windows)
1. Install Python if it is not already installed.
2. Open PowerShell in this folder.
3. Install dependencies:
   `py -m pip install -r requirements.txt`
4. Copy `stocks_cleaned.csv` into this same folder, beside `app.py`.
5. Run:
   `py -m streamlit run app.py`

The app expects these columns:
`date`, `open`, `high`, `low`, `close`, `volume`, `Name`.
It also uses `daily_return` and `year`; if either is missing, it attempts to create it.

The app uses a sample of up to 5,000 rows for the volume/return scatter plot to keep rendering manageable.
