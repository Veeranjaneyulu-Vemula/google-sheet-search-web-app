
from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load JSON from environment variable
creds_json = os.getenv("GOOGLE_CREDS_JSON")
if not creds_json:
    raise ValueError("GOOGLE_CREDS_JSON not set in environment.")

# Parse the JSON string into a Python dict
creds_dict = json.loads(creds_json)

# Use credentials
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Mediation_DB_V2").sheet1  # Replace with your actual Google Sheet name

@app.route('/', methods=['GET', 'POST'])
def search():
    results = []
    query = ""

    if request.method == 'POST':
        query = request.form['query'].lower()
        data = sheet.get_all_records()

        for row in data:
            if any(query in str(value).lower() for value in row.values()):
                results.append(row)

    return render_template('search.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
