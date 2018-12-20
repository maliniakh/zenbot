import tensorflow as tf
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.utils import shuffle
import time
import labels
import matplotlib.pyplot as plt
import data


def create_file_reader_ops(filename):
    headers = get_csv_headers(filename)
    record_defaults = list(map(lambda h: [0.0] if "trend" in h else [0.0], headers))

    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TextLineReader(skip_header_lines=1)
    _, csv_row = reader.read(filename_queue)
    columns = tf.decode_csv(csv_row, record_defaults=record_defaults)

    #features
    features = []
    label = _
    for h, c in zip(headers, columns):
        if("back" in h):
            features.append(c)
        if(h == "trend"):
            label = c

    features = tf.stack(features)
    # label.py = tf.one_hot(indices=[0, 2], depth=3)
    label = tf.stack(label)
    return features, label

def get_csv_headers(filename):
    with open(filename) as fp:
        line = fp.readline()
        return np.asarray(list(map(lambda s: s.strip(), line.split(","))))




filename = "/home/maliniak/code/zenbot/simulations/merged-binance.csv"
# features, label.py = create_file_reader_ops(filename)

# low_memory : boolean, default True?
csv = pd.read_csv(filename, low_memory=False)
csv = shuffle(csv)
(train_x, train_y, test_x, test_y) = data.get_data(csv)

model = tf.keras.models.Sequential([
  # tf.keras.layers.Dense(100, activation=tf.nn.sigmoid),
  #   tf.keras.layers.Conv1D(32, 7,activation=tf.nn.sigmoid),
    # tf.keras..layers.Flatten(),
  tf.keras.layers.Dense(80, activation=tf.nn.tanh, input_shape=(train_x.shape[1],)),
  tf.keras.layers.Dense(20, activation=tf.nn.tanh),              # z relu wychodzily nany same
  tf.keras.layers.Dense(1, activation=tf.nn.relu)
])

# sgd = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(optimizer='adam',
              #sparse_categorical_crossentropy
              #loss='categorical_crossentropy',
              loss='mean_squared_error',
              metrics=['accuracy'])

model.fit(train_x, train_y, epochs=1)
test_loss, test_acc = model.evaluate(test_x, test_y)
print('Test: ', test_acc, " ", test_loss)

model_filename = 'model/model.{}.{}.h5'.format(time.strftime("%Y%m%d%H%M"), int(100*test_acc))
model.save(model_filename)
print("Model saved to " + model_filename)

x, y, close_abs, maxinday = data.get_data(pd.read_csv('/home/maliniak/code/zenbot/simulations/sim_result_binance.STEEM-BTC_181218_151700.csv', low_memory=False), split=1)
predict = model.predict(x)

# for i in range(100):,
#     print(np.round(y[i], 2), "\t", np.round(predict[i], 2))

predicted_abs = []
real_max_in_day = []
for i in range(y.shape[0]):
    predicted_abs.append(close_abs[i] * predict[i])
    real_max_in_day.append(close_abs[i] * maxinday[i])

fig, ax = plt.subplots()
ax.plot(close_abs, 'r', predicted_abs, 'b', real_max_in_day, 'g')
ax.grid(True)
fig.autofmt_xdate()
plt.show()


i = 2
# for i in range(10):
# print(lb.classes_)
# predict = model.predict(test_x)






