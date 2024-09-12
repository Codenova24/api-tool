from flask import Flask, render_template, request
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    error = None
    
    if request.method == 'POST':
        url = request.form.get('url')
        method = request.form.get('method')
        headers_str = request.form.get('headers')
        data_str = request.form.get('data')

        # Convert headers from JSON string to dictionary
        try:
            headers = json.loads(headers_str) if headers_str else {}
        except json.JSONDecodeError:
            error = 'Invalid headers format. Ensure it is valid JSON.'

        # Convert data based on the method
        data = data_str if data_str else None

        if not error:
            try:
                response = requests.request(method, url, headers=headers, data=data)
            except requests.RequestException as e:
                error = str(e)

    return render_template('index.html', response=response, error=error)

if __name__ == '__main__':
    app.run(debug=True)
