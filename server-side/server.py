from flask import Flask, request, jsonify
from face_labeler import emojify
app = Flask(__name__)

_numPics = 0

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/get_image', methods=['POST'])
def get_image():
    global _numPics
    image = request.form['image']
    # print(image)

    emojified_image = emojify(image, _numPics)
    _numPics += 1
    return image

app.run(host='0.0.0.0', debug=True, threaded=True)
