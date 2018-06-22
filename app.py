import json
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return send_file("./static/index.html")

@app.route('/foo', methods=['GET'])
def foo():
    # print('hello')
    # print(dir(request.form))
    # print(request.form.to_dict())
    return jsonify({"a": 1, "b": 2, "c": 3})
    # return "True"


app.run(debug=True)