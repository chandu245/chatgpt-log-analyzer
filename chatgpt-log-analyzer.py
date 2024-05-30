from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import openai
import json
import logging

app = Flask(__name__)

# Initialize Elasticsearch client with your Elasticsearch instance URL
es = Elasticsearch("http://127.0.0.1:9200") #connecting to local elk instance

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key' #get yours from https://platform.openai.com/api-keys

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def generate_es_query(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates Elasticsearch queries from natural language input. Only return the JSON of the query, without any additional text."},
            {"role": "user", "content": user_input}
        ]
    )
    es_query = response.choices[0].message['content'].strip()
    logging.debug(f"Generated Elasticsearch query: {es_query}")
    return es_query

def summarize_and_advise(results):
    logs_text = "\n".join([json.dumps(result['_source']) for result in results])
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes log entries and provides advice."},
            {"role": "user", "content": f"Summarize and advise on the following log entries:\n{logs_text}"}
        ]
    )
    summary_and_advice = response.choices[0].message['content'].strip()
    logging.debug(f"Generated summary and advice: {summary_and_advice}")
    return summary_and_advice

@app.route('/query', methods=['POST'])
def query():
    if request.is_json:
        user_input = request.json.get('query')
        if not user_input:
            return jsonify({"error": "Query is missing"}), 400
        try:
            es_query = generate_es_query(user_input)
            es_query_json = json.loads(es_query)
            response = es.search(index="your_index_name", body=es_query_json)
            results = response['hits']['hits']
            summary_and_advice = summarize_and_advise(results)
            return jsonify({"summary_and_advice": summary_and_advice})
        except json.JSONDecodeError as json_err:
            logging.error(f"JSON decoding error: {json_err}")
            return jsonify({"error": "Invalid query generated"}), 500
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid content type, expected application/json"}), 400

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatGPT Log Analysis</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body, html {
                height: 100%;
                margin: 0;
            }
            .bg {
                background-image: url('https://c0.wallpaperflare.com/preview/997/717/184/artificial-intelligence-codes-developing-screen.jpg');
                height: 100%; 
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }
            .centered-form {
                height: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .form-container {
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 600px;
            }
            #searching-message {
                display: none;
                text-align: center;
                margin-top: 10px;
            }
            .spinner-border {
                width: 3rem;
                height: 3rem;
            }
            #summary-and-advice {
                margin-top: 10px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                white-space: pre-wrap;
                max-height: 300px; /* Set a max height for the summary and advice box */
                overflow-y: auto; /* Add scroll functionality if content overflows */
            }
        </style>
    </head>
    <body>
        <div class="bg">
            <div class="centered-form">
                <div class="form-container">
                    <form id="query-form">
                        <div class="form-group">
                            <input type="text" id="query" name="query" class="form-control" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Search</button>
                    </form>
                    <div id="searching-message">
                        <div class="spinner-border text-primary" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                        <div>Analyzing the logs, wait for summary & advice...</div>
                    </div>
                    <div id="summary-and-advice" class="mt-4"></div>
                </div>
            </div>
        </div>
        <script>
            document.getElementById('query-form').addEventListener('submit', async function(event) {
                event.preventDefault();
                const query = document.getElementById('query').value;
                const searchingMessage = document.getElementById('searching-message');
                const summaryAndAdviceContainer = document.getElementById('summary-and-advice');
                searchingMessage.style.display = 'block';
                summaryAndAdviceContainer.innerText = '';
                try {
                    const response = await fetch('/query', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ query: query })
                    });
                    const data = await response.json();
                    summaryAndAdviceContainer.innerText = data.summary_and_advice;
                } catch (error) {
                    summaryAndAdviceContainer.innerText = 'An error occurred: ' + error.message;
                } finally {
                    searchingMessage.style.display = 'none';
                }
            });
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True,port=8080) #default is port 5000

