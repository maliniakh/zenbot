import tensorflow as tf
from flask import Flask

model = tf.keras.models.load_model('model/model.201811121939.48.h5')
# model.predict([1,2,3,4])



app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
