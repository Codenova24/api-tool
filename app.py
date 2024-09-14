from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session

# Initialize request history in the session if not already present
def initialize_history():
    if 'request_history' not in session:
        session['request_history'] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    response_data = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url')
        method = request.form.get('method')
        headers = request.form.get('headers')
        data = request.form.get('data')

        # Process headers and data
        try:
            headers_dict = eval(headers) if headers else {}
            data_dict = eval(data) if data else {}
        except Exception as e:
            error = "Invalid JSON format in headers or data."
            return render_template('index.html', response_data=None, error=error)

        # Make the API request
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers_dict)
            elif method == 'POST':
                response = requests.post(url, headers=headers_dict, json=data_dict)
            elif method == 'PUT':
                response = requests.put(url, headers=headers_dict, json=data_dict)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers_dict)
            else:
                error = "Unsupported HTTP method."
                return render_template('index.html', response_data=None, error=error)

            # Store the request and response in the session history
            initialize_history()
            session['request_history'].append({
                'url': url,
                'method': method,
                'headers': headers,
                'data': data,
                'status_code': response.status_code,
                'response_headers': dict(response.headers),
                'response_body': response.text
            })

            response_data = response
        except Exception as e:
            error = f"Error making the request: {e}"

    # Render the index with the response and history
    return render_template('index.html', response_data=response_data, error=error, history=session.get('request_history'))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('request_history', None)  # Clear the history
    return jsonify({'message': 'History cleared successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
