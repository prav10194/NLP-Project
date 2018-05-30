from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from Part2 import get_documents, get_features
import re

app = Flask(__name__,static_folder='static')

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/getDocuments')
def getDocuments():
    # query = request.args.get("query")
    print("Called getDocuments()")
    # print(query)
    documents = get_documents()

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    documents_sorted = sorted(documents, key = alphanum_key)

    print("Documents: " + str(documents_sorted))
    return jsonify(documents_sorted)


@app.route('/getFeatures')
def getFeatures():
    filename = request.args.get("filename")
    print("Called getFeatures()")
    # print(filename)
    text = get_features(filename)
    # print(text)
    return text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
