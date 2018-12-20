import pandas as pd
from pandas import DataFrame


def get_data(df: DataFrame, split: float=0.9):
    """
    :param df:
    :type split: float jak 1 to zwraca tylko (train_x, train_y, close_abs)
    """
    # df = df[:10000]

    df = df.loc[:, [c for c in list(df.columns) if 'cci' not in c]] #cci jest nan, moze dlatego
    # bierzemy tylko te kolumny co sie zaczynaja od back*, taka konwencja
    # todo: volume dodac, ale musi byc znormalizowany (wzledem sredniej z ostatnich dni np)
    x = df.loc[:, [c for c in list(df.columns) if
                   c.startswith('back')
                   and not 'volume' not in c]].values.astype('float32')
    # [c for c in list(df.columns) if
    # not c.startswith('ahead')
    # and c != 'trend'
    # and c != 'maxinday' and c != 'mininday'
    # and 'close_abs' not in c]
    y = df.loc[:, 'maxinday'].values
    # y = labels.binarize(y)
    rows_no = df.shape[0]
    split_idx = int(rows_no * split)
    train_x = x[:split_idx]
    train_y = y[:split_idx]
    test_x = x[split_idx:]
    test_y = y[split_idx:]

    if(split == 1):
        close_abs = df.loc[:, ['close_abs']].values.astype('float32')
        maxinday = df.loc[:, ['maxinday']].values.astype('float32')
        return train_x, train_y, close_abs, maxinday

    return train_x, train_y, test_x, test_y