from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from Part3 import find_documents, get_text

app = Flask(__name__,static_folder='static')

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/getResults')
def getResults():
    query = request.args.get("query")
    print("Called getResults()")
    # print(query)
    documents = find_documents(query)
    return jsonify(documents)


@app.route('/getText')
def getText():
    filename = request.args.get("filename")
    print("Called getText()")
    # print(filename)
    text = get_text(filename)
    # print(text)
    return text

if __name__ == '__main__':
    app.run(debug=True,port=5002)
