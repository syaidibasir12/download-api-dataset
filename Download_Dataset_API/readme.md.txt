# ContactSpace Data Downloader

A Python script to fetch and export applicant records from the ContactSpace API for multiple initiatives.

## Features
- Connects to ContactSpace API using initiative and dataset IDs.
- Fetches all pages of applicant data.
- Dynamically creates CSV files per initiative.
- Handles missing columns and ensures consistent formatting.

## Requirements
- Python 3.8+
- `requests`
- `pandas`

Install dependencies:
```bash
pip install -r requirements.txt
