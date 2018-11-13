import tensorflow as tf
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import MultiLabelBinarizer, LabelBinarizer
from sklearn.utils import shuffle
from tensorflow.python.keras import optimizers
import time



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
    # label = tf.one_hot(indices=[0, 2], depth=3)
    label = tf.stack(label)
    return features, label

def get_csv_headers(filename):
    with open(filename) as fp:
        line = fp.readline()
        return np.asarray(list(map(lambda s: s.strip(), line.split(","))))

def get_data(df: DataFrame):
    # df = df[:10000]
    df = df.loc[:, [c for c in list(df.columns) if 'cci' not in c]] #cci jest nan, moze dlatego
    x = df.loc[:, [c for c in list(df.columns) if not c.startswith('ahead') and c != 'trend']].values.astype('float32')
    y = df.loc[:, 'trend'].values
    lb = LabelBinarizer()
    y = lb.fit_transform(y)
    rows_no = df.shape[0]
    split_idx = int(rows_no * 0.9)
    train_x = x[:split_idx]
    train_y = y[:split_idx]
    test_x = x[split_idx:]
    test_y = y[split_idx:]
    return (train_x, train_y, test_x, test_y, lb)


filename = "/home/maliniak/code/zenbot/simulations/merged.csv"
# features, label = create_file_reader_ops(filename)

# low_memory : boolean, default True?
csv = pd.read_csv(filename)
csv = shuffle(csv)
(train_x, train_y, test_x, test_y, lb) = get_data(csv)

model = tf.keras.models.Sequential([
  # tf.keras.layers.Dense(100, activation=tf.nn.sigmoid),
  #   tf.keras.layers.Conv1D(32, 7,activation=tf.nn.sigmoid),
    # tf.keras..layers.Flatten(),
  tf.keras.layers.Dense(80, activation=tf.nn.sigmoid, input_shape=(train_x.shape[1],)),
  tf.keras.layers.Dense(20, activation=tf.nn.sigmoid),              # z relu wychodzily nany same
  tf.keras.layers.Dense(3, activation=tf.nn.sigmoid)
])

# sgd = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(optimizer='adam',
              #sparse_categorical_crossentropy
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_x, train_y, epochs=1)
test_loss, test_acc = model.evaluate(test_x, test_y)
print('Test: ', test_acc, " ", test_loss)

model_filename = 'model.{}.{}.h5'.format(time.strftime("%Y%m%d%H%M"), int(100*test_acc))
model.save(model_filename)
print("Model saved to " + model_filename)


# for i in range(10):
print(lb.classes_)
predict = model.predict(test_x)
for i in range(5):
    print(np.round(test_y[i], 2), "\n", np.round(predict[i], 2))





