import tensorflow as tf
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.utils import shuffle
import time
import labels

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


def get_data(df: DataFrame, split: float=0.9):
    """
    :param df:
    :type split: float jak 1 to zwraca tylko (train_x, train_y, close_abs)
    """
    # df = df[:10000]
    df = df.loc[:, [c for c in list(df.columns) if 'cci' not in c]] #cci jest nan, moze dlatego
    x = df.loc[:, [c for c in list(df.columns) if
                   not c.startswith('ahead')
                   and c != 'trend'
                   and c != 'maxinday' and c != 'mininday'
                   and 'close_abs' not in c]].values.astype('float32')
    y = df.loc[:, 'maxinday'].values
    # y = labels.binarize(y)
    rows_no = df.shape[0]
    split_idx = int(rows_no * split)
    train_x = x[:split_idx]
    train_y = y[:split_idx]
    test_x = x[split_idx:]
    test_y = y[split_idx:]

    if(split == 1):
        close_abs = df.loc[:, ['back0.close_abs']].values.astype('float32')
        return train_x, train_y, close_abs

    return train_x, train_y, test_x, test_y


filename = "/home/maliniak/code/zenbot/simulations/merged.csv"
# features, label.py = create_file_reader_ops(filename)

# low_memory : boolean, default True?
csv = pd.read_csv(filename, low_memory=False)
csv = shuffle(csv)
(train_x, train_y, test_x, test_y) = get_data(csv)

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

x, y, close_abs = get_data(pd.read_csv('/home/maliniak/code/zenbot/simulations/merged-binance.ADA-BTC.csv', low_memory=False), split=1)
predict = model.predict(x)

for i in range(100):
    print(np.round(y[i], 2), "\t", np.round(predict[i], 2))

# for i in range(10):
# print(lb.classes_)
# predict = model.predict(test_x)






