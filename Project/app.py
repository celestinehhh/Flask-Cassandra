import os
import time
import numpy as np
from flask import Flask, jsonify, request, abort
from PIL import Image
import tensorflow as tf
import Mycas

app = Flask(__name__)
class_names = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt',
    'Sneaker', 'Bag', 'Ankle boot'
]
Mycas.createKeySpace()


def preprocess(pic):
    pic = Image.open(pic).convert('L')
    pic.show()
    pic = pic.resize((28, 28))
    pic.show()
    pic = np.array(pic).reshape((1, 28, 28))
    return pic / 255.0


def predict(pic):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER + '/data', 'my_model.h5')
    probability_model = tf.keras.models.load_model(my_file)
    print("model loaded")
    predictions = probability_model.predict(pic)
    print("predict:")
    label = np.argmax(predictions[0])
    return label


def time_now():
    ticks = time.time()
    tm_struct = time.localtime(ticks)
    time_str = time.asctime(tm_struct)
    print(time_str)
    return time_str


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/GSY')
def hello_gsy():
    return 'Hello, GSY!'


@app.route('/api/tasks/upload', methods=['POST'])
def upload():
    img_bin = request.files['image']
    image_name = request.files['image'].filename
    if not img_bin:
        return ("请上传一张jpg图片")
    img_bin.save(image_name)
    print("上传成功")
    new_pic = preprocess(image_name)
    print("picture preprocessed")
    print(new_pic.shape)
    print("successful")
    label = predict(new_pic)
    print(class_names[label])
    Mycas.Insert(time_now(), image_name, class_names[label])
    return str(class_names[label])


@app.route('/api/tasks', methods=['GET'])
def list_all():
    tasks = []
    rows = Mycas.Show_All()
    id = 1
    for row in rows:
        task = {'id': id}
        task['time'] = row[0]
        task['image_name'] = row[1]
        task['class_name'] = row[2]
        tasks.append(task)
        id += 1
    return jsonify(tasks), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
