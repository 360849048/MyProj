from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return send_file("./static/index.html")

@app.route('/foo', methods=['POST'])
def foo():
    print('hello')
    # print(dir(request.form))
    print(request.form.to_dict())
    return "True"


app.run(debug=True)