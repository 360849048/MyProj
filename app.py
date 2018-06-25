import json
from flask import Flask, request, send_file, jsonify
from pysrc.sqljob import TableManager

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return send_file("./static/index.html")

@app.route('/foo', methods=['GET'])
def foo():
    # print('hello')
    # print(dir(request.form))
    # print(request.form.to_dict())

    inputs = {}
    t_di = TableManager('digital_input', './libfiles/data.db')
    for id in t_di.getAllId():
        inputs[str(id)] = t_di.displayBriefData(id, 'id', 'CName')[1]


    return jsonify(inputs)

@app.route('/io', methods=['GET'])
def getDi():
    io_type = request.args.get('type')
    start_id = int(request.args.get('start'))
    end_id = int(request.args.get('end'))
    if io_type == 'di':
        t_io = TableManager('digital_input', './libfiles/data.db')
    elif io_type == 'do':
        t_io = TableManager('digital_output', './libfiles/data.db')
    elif io_type == 'ai':
        t_io = TableManager('analog_input', './libfiles/data.db')
    else:
        t_io = TableManager('analog_output', './libfiles/data.db')
    ret_data = {}
    ret_data['amount'] = len(t_io.getAllId())           # 每次都会重新查询，性能或许可以优化
    ret_data['ios'] = {}
    if start_id > end_id or start_id > ret_data['amount']:
        return jsonify(ret_data)
    if end_id > ret_data['amount']:
        end_id = ret_data['amount']
    for id in range(start_id, end_id + 1):
        ret_data['ios'][str(id)] = t_io.displayBriefData(id, 'id', 'CName')[1]

    return jsonify(ret_data)


# app.run(host='172.18.71.158', port=8080)
app.run(debug=True)