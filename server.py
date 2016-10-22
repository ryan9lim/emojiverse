from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/get_image', methods=['POST'])
def get_image():
    image = request.form['image']
    return image

app.run(host='0.0.0.0', debug=True, threaded=True)
