from flask import Flask, request, jsonify
from retriever import retrieve_information  # Import your working retriever function

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/', methods=['POST'])
def retrieve():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400

    query = data['query']
    result = retrieve_information(query)
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
