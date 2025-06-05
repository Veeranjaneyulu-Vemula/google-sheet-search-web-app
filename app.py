
from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
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
