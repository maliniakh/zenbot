import tensorflow as tf
import numpy as np
from flask import Flask, jsonify, request

from labels import frombin

model = tf.keras.models.load_model('model/model.201811121939.48.h5')
model._make_predict_function()

# model.predict([1,2,3,4])

app = Flask(__name__)


@app.route("/fit", methods=['POST'])
def fit():
    print(request.json.get('thing2'))
    input_arr = []

    # todo: sprawdzic raz na poczatku kolejnosc keys np
    for k in request.json.keys():
        input_arr.append(request.json.get(k))

    prediction = model.predict(np.asarray([np.asarray(input_arr)]))
    return frombin(prediction[0])


if __name__ == '__main__':
    app.run(debug=True)
